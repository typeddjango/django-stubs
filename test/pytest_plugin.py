import dataclasses
import inspect
import os
import sys
import tempfile
import textwrap
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Any, Optional, cast, List, Type, Callable, Dict

import pytest
from _pytest._code.code import ReprFileLocation, ReprEntry, ExceptionInfo
from decorator import decorate
from mypy import api as mypy_api

from test import vistir
from test.helpers import assert_string_arrays_equal, TypecheckAssertionError, expand_errors, get_func_first_lnum


def reveal_type(obj: Any) -> None:
    # noop method, just to get rid of "method is not resolved" errors
    pass


def output(output_lines: str):
    def decor(func: Callable[..., None]):
        func.out = output_lines

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return decorate(func, wrapper)

    return decor


def get_class_that_defined_method(meth) -> Type['MypyTypecheckTestCase']:
    if inspect.ismethod(meth):
        for cls in inspect.getmro(meth.__self__.__class__):
            if cls.__dict__.get(meth.__name__) is meth:
                return cls
        meth = meth.__func__  # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        cls = getattr(inspect.getmodule(meth),
                      meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
        if issubclass(cls, MypyTypecheckTestCase):
            return cls
    return getattr(meth, '__objclass__', None)  # handle special descriptor objects


def file(filename: str, make_parent_packages=False):
    def decor(func: Callable[..., None]):
        func.filename = filename
        func.make_parent_packages = make_parent_packages
        return func

    return decor


def env(**environ):
    def decor(func: Callable[..., None]):
        func.env = environ
        return func

    return decor


@dataclasses.dataclass
class CreateFile:
    sources: str
    make_parent_packages: bool = False


class MypyTypecheckMeta(type):
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        cls.files: Dict[str, CreateFile] = {}

        for name, attr in attrs.items():
            if inspect.isfunction(attr):
                filename = getattr(attr, 'filename', None)
                if not filename:
                    continue
                make_parent_packages = getattr(attr, 'make_parent_packages', False)
                sources = textwrap.dedent(''.join(get_func_first_lnum(attr)[1]))
                if sources.strip() == 'pass':
                    sources = ''
                cls.files[filename] = CreateFile(sources, make_parent_packages)

        return cls


class MypyTypecheckTestCase(metaclass=MypyTypecheckMeta):
    files = None

    def ini_file(self) -> str:
        return """
[mypy]
        """

    def _get_ini_file_contents(self) -> Optional[str]:
        raw_ini_file = self.ini_file()
        if not raw_ini_file:
            return raw_ini_file
        return raw_ini_file.strip() + '\n'


class TraceLastReprEntry(ReprEntry):
    def toterminal(self, tw):
        self.reprfileloc.toterminal(tw)
        for line in self.lines:
            red = line.startswith("E   ")
            tw.line(line, bold=True, red=red)
        return


def fname_to_module(fpath: Path, root_path: Path) -> Optional[str]:
    try:
        relpath = fpath.relative_to(root_path).with_suffix('')
        return str(relpath).replace(os.sep, '.')
    except ValueError:
        return None


class MypyTypecheckItem(pytest.Item):
    root_directory = '/run/testdata'

    def __init__(self,
                 name: str,
                 parent: 'MypyTestsCollector',
                 klass: Type[MypyTypecheckTestCase],
                 source_code: str,
                 first_lineno: int,
                 ini_file_contents: Optional[str] = None,
                 expected_output_lines: Optional[List[str]] = None,
                 files: Optional[Dict[str, CreateFile]] = None,
                 custom_environment: Optional[Dict[str, Any]] = None):
        super().__init__(name=name, parent=parent)
        self.klass = klass
        self.source_code = source_code
        self.first_lineno = first_lineno
        self.ini_file_contents = ini_file_contents
        self.expected_output_lines = expected_output_lines
        self.files = files
        self.custom_environment = custom_environment

    @contextmanager
    def temp_directory(self) -> Path:
        with tempfile.TemporaryDirectory(prefix='mypy-pytest-',
                                         dir=self.root_directory) as tmpdir_name:
            yield Path(self.root_directory) / tmpdir_name

    def runtest(self):
        with self.temp_directory() as tmpdir_path:
            if not self.source_code:
                return

            if self.ini_file_contents:
                mypy_ini_fpath = tmpdir_path / 'mypy.ini'
                mypy_ini_fpath.write_text(self.ini_file_contents)

            test_specific_modules = []
            for fname, create_file in self.files.items():
                fpath = tmpdir_path / fname
                if create_file.make_parent_packages:
                    fpath.parent.mkdir(parents=True, exist_ok=True)
                    for parent in fpath.parents:
                        try:
                            parent.relative_to(tmpdir_path)
                            if parent != tmpdir_path:
                                parent_init_file = parent / '__init__.py'
                                parent_init_file.write_text('')
                                test_specific_modules.append(fname_to_module(parent,
                                                                             root_path=tmpdir_path))
                        except ValueError:
                            break

                fpath.write_text(create_file.sources)
                test_specific_modules.append(fname_to_module(fpath,
                                                             root_path=tmpdir_path))

            with vistir.temp_environ(), vistir.temp_path():
                for key, val in (self.custom_environment or {}).items():
                    os.environ[key] = val
                sys.path.insert(0, str(tmpdir_path))

                mypy_cmd_options = self.prepare_mypy_cmd_options(config_file_path=mypy_ini_fpath)
                main_fpath = tmpdir_path / 'main.py'
                main_fpath.write_text(self.source_code)
                mypy_cmd_options.append(str(main_fpath))

                stdout, stderr, returncode = mypy_api.run(mypy_cmd_options)
                output_lines = []
                for line in (stdout + stderr).splitlines():
                    if ':' not in line:
                        continue
                    out_fpath, res_line = line.split(':', 1)
                    line = os.path.relpath(out_fpath, start=tmpdir_path) + ':' + res_line
                    output_lines.append(line.strip().replace('.py', ''))

                for module in test_specific_modules:
                    parts = module.split('.')
                    for i in range(len(parts)):
                        parent_module = '.'.join(parts[:i + 1])
                        if parent_module in sys.modules:
                            del sys.modules[parent_module]

                assert_string_arrays_equal(expected=self.expected_output_lines,
                                           actual=output_lines)

    def prepare_mypy_cmd_options(self, config_file_path: Path) -> List[str]:
        mypy_cmd_options = [
            '--raise-exceptions',
            '--no-silence-site-packages'
        ]
        python_version = '.'.join([str(part) for part in sys.version_info[:2]])
        mypy_cmd_options.append(f'--python-version={python_version}')
        if self.ini_file_contents:
            mypy_cmd_options.append(f'--config-file={config_file_path}')
        return mypy_cmd_options

    def repr_failure(self, excinfo: ExceptionInfo) -> str:
        if excinfo.errisinstance(SystemExit):
            # We assume that before doing exit() (which raises SystemExit) we've printed
            # enough context about what happened so that a stack trace is not useful.
            # In particular, uncaught exceptions during semantic analysis or type checking
            # call exit() and they already print out a stack trace.
            return excinfo.exconly(tryshort=True)
        elif excinfo.errisinstance(TypecheckAssertionError):
            # with traceback removed
            exception_repr = excinfo.getrepr(style='short')
            exception_repr.reprcrash.message = ''
            repr_file_location = ReprFileLocation(path=inspect.getfile(self.klass),
                                                  lineno=self.first_lineno + excinfo.value.lineno,
                                                  message='')
            repr_tb_entry = TraceLastReprEntry(filelocrepr=repr_file_location,
                                               lines=exception_repr.reprtraceback.reprentries[-1].lines[1:],
                                               style='short',
                                               reprlocals=None,
                                               reprfuncargs=None)
            exception_repr.reprtraceback.reprentries = [repr_tb_entry]
            return exception_repr
        else:
            return super().repr_failure(excinfo, style='native')

    def reportinfo(self):
        return self.fspath, None, get_class_qualname(self.klass) + '::' + self.name


def get_class_qualname(klass: type) -> str:
    return klass.__module__ + '.' + klass.__name__


def extract_test_output(attr: Callable[..., None]) -> List[str]:
    out_data: str = getattr(attr, 'out', None)
    out_lines = []
    if out_data:
        for line in out_data.split('\n'):
            line = line.strip()
            out_lines.append(line)
    return out_lines


class MypyTestsCollector(pytest.Class):
    def get_ini_file_contents(self, contents: str) -> str:
        return contents.strip() + '\n'

    def collect(self) -> Iterator[pytest.Item]:
        current_testcase = cast(MypyTypecheckTestCase, self.obj())
        ini_file_contents = self.get_ini_file_contents(current_testcase.ini_file())
        for attr_name in dir(current_testcase):
            if attr_name.startswith('test_'):
                attr = getattr(self.obj, attr_name)
                if inspect.isfunction(attr):
                    first_line_lnum, source_lines = get_func_first_lnum(attr)
                    func_first_line_in_file = inspect.getsourcelines(attr)[1] + first_line_lnum

                    output_from_decorator = extract_test_output(attr)
                    output_from_comments = expand_errors(source_lines, 'main')
                    custom_env = getattr(attr, 'env', None)
                    main_source_code = textwrap.dedent(''.join(source_lines))
                    yield MypyTypecheckItem(name=attr_name,
                                            parent=self,
                                            klass=current_testcase.__class__,
                                            source_code=main_source_code,
                                            first_lineno=func_first_line_in_file,
                                            ini_file_contents=ini_file_contents,
                                            expected_output_lines=output_from_comments
                                                                  + output_from_decorator,
                                            files=current_testcase.__class__.files,
                                            custom_environment=custom_env)


def pytest_pycollect_makeitem(collector: Any, name: str, obj: Any) -> Optional[MypyTestsCollector]:
    # Only classes derived from DataSuite contain test cases, not the DataSuite class itself
    if (isinstance(obj, type)
            and issubclass(obj, MypyTypecheckTestCase)
            and obj is not MypyTypecheckTestCase):
        # Non-None result means this obj is a test case.
        # The collect method of the returned DataSuiteCollector instance will be called later,
        # with self.obj being obj.
        return MypyTestsCollector(name, parent=collector)
