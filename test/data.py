import os
import posixpath
import re
import sys
import tempfile
from typing import Any, Optional, Iterator, Dict, List, Tuple, Set

import pytest
from mypy.test.config import test_temp_dir
from mypy.test.data import DataDrivenTestCase, DataSuite, add_test_name_suffix, parse_test_data, \
    expand_errors, expand_variables, fix_win_path


def parse_test_case(case: 'DataDrivenTestCase') -> None:
    """Parse and prepare a single case from suite with test case descriptions.

    This method is part of the setup phase, just before the test case is run.
    """
    test_items = parse_test_data(case.data, case.name)
    base_path = case.suite.base_path
    if case.suite.native_sep:
        join = os.path.join
    else:
        join = posixpath.join  # type: ignore

    out_section_missing = case.suite.required_out_section

    files = []  # type: List[Tuple[str, str]] # path and contents
    output_files = []  # type: List[Tuple[str, str]] # path and contents for output files
    output = []  # type: List[str]  # Regular output errors
    output2 = {}  # type: Dict[int, List[str]]  # Output errors for incremental, runs 2+
    deleted_paths = {}  # type: Dict[int, Set[str]]  # from run number of paths
    stale_modules = {}  # type: Dict[int, Set[str]]  # from run number to module names
    rechecked_modules = {}  # type: Dict[ int, Set[str]]  # from run number module names
    triggered = []  # type: List[str]  # Active triggers (one line per incremental step)

    # Process the parsed items. Each item has a header of form [id args],
    # optionally followed by lines of text.
    item = first_item = test_items[0]
    for item in test_items[1:]:
        if item.id == 'file' or item.id == 'outfile':
            # Record an extra file needed for the test case.
            assert item.arg is not None
            contents = expand_variables('\n'.join(item.data))
            file_entry = (join(base_path, item.arg), contents)
            if item.id == 'file':
                files.append(file_entry)
            else:
                output_files.append(file_entry)
        elif item.id in ('builtins', 'builtins_py2'):
            # Use an alternative stub file for the builtins module.
            assert item.arg is not None
            mpath = join(os.path.dirname(case.file), item.arg)
            fnam = 'builtins.pyi' if item.id == 'builtins' else '__builtin__.pyi'
            with open(mpath) as f:
                files.append((join(base_path, fnam), f.read()))
        elif item.id == 'typing':
            # Use an alternative stub file for the typing module.
            assert item.arg is not None
            src_path = join(os.path.dirname(case.file), item.arg)
            with open(src_path) as f:
                files.append((join(base_path, 'typing.pyi'), f.read()))
        elif re.match(r'stale[0-9]*$', item.id):
            passnum = 1 if item.id == 'stale' else int(item.id[len('stale'):])
            assert passnum > 0
            modules = (set() if item.arg is None else {t.strip() for t in item.arg.split(',')})
            stale_modules[passnum] = modules
        elif re.match(r'rechecked[0-9]*$', item.id):
            passnum = 1 if item.id == 'rechecked' else int(item.id[len('rechecked'):])
            assert passnum > 0
            modules = (set() if item.arg is None else {t.strip() for t in item.arg.split(',')})
            rechecked_modules[passnum] = modules
        elif item.id == 'delete':
            # File to delete during a multi-step test case
            assert item.arg is not None
            m = re.match(r'(.*)\.([0-9]+)$', item.arg)
            assert m, 'Invalid delete section: {}'.format(item.arg)
            num = int(m.group(2))
            assert num >= 2, "Can't delete during step {}".format(num)
            full = join(base_path, m.group(1))
            deleted_paths.setdefault(num, set()).add(full)
        elif re.match(r'out[0-9]*$', item.id):
            tmp_output = [expand_variables(line) for line in item.data]
            if os.path.sep == '\\':
                tmp_output = [fix_win_path(line) for line in tmp_output]
            if item.id == 'out' or item.id == 'out1':
                output = tmp_output
            else:
                passnum = int(item.id[len('out'):])
                assert passnum > 1
                output2[passnum] = tmp_output
            out_section_missing = False
        elif item.id == 'triggered' and item.arg is None:
            triggered = item.data
        elif item.id == 'env':
            env_vars_to_set = item.arg
            for env in env_vars_to_set.split(';'):
                try:
                    name, value = env.split('=')
                    os.environ[name] = value
                except ValueError:
                    continue
        else:
            raise ValueError(
                'Invalid section header {} in {} at line {}'.format(
                    item.id, case.file, item.line))

    if out_section_missing:
        raise ValueError(
            '{}, line {}: Required output section not found'.format(
                case.file, first_item.line))

    for passnum in stale_modules.keys():
        if passnum not in rechecked_modules:
            # If the set of rechecked modules isn't specified, make it the same as the set
            # of modules with a stale public interface.
            rechecked_modules[passnum] = stale_modules[passnum]
        if (passnum in stale_modules
                and passnum in rechecked_modules
                and not stale_modules[passnum].issubset(rechecked_modules[passnum])):
            raise ValueError(
                ('Stale modules after pass {} must be a subset of rechecked '
                 'modules ({}:{})').format(passnum, case.file, first_item.line))

    input = first_item.data
    expand_errors(input, output, 'main')
    for file_path, contents in files:
        expand_errors(contents.split('\n'), output, file_path)

    case.input = input
    case.output = output
    case.output2 = output2
    case.lastline = item.line
    case.files = files
    case.output_files = output_files
    case.expected_stale_modules = stale_modules
    case.expected_rechecked_modules = rechecked_modules
    case.deleted_paths = deleted_paths
    case.triggered = triggered or []


class DjangoDataDrivenTestCase(DataDrivenTestCase):
    def setup(self) -> None:
        self.old_environ = os.environ.copy()

        parse_test_case(case=self)
        self.old_cwd = os.getcwd()

        self.tmpdir = tempfile.TemporaryDirectory(prefix='mypy-test-')
        tmpdir_root = os.path.join(self.tmpdir.name, 'tmp')

        new_files = []
        for path, contents in self.files:
            new_files.append((path, contents.replace('<TMP>', tmpdir_root)))
        self.files = new_files

        os.chdir(self.tmpdir.name)
        os.mkdir(test_temp_dir)
        encountered_files = set()
        self.clean_up = []
        for paths in self.deleted_paths.values():
            for path in paths:
                self.clean_up.append((False, path))
                encountered_files.add(path)
        for path, content in self.files:
            dir = os.path.dirname(path)
            for d in self.add_dirs(dir):
                self.clean_up.append((True, d))
            with open(path, 'w') as f:
                f.write(content)
            if path not in encountered_files:
                self.clean_up.append((False, path))
                encountered_files.add(path)
            if re.search(r'\.[2-9]$', path):
                # Make sure new files introduced in the second and later runs are accounted for
                renamed_path = path[:-2]
                if renamed_path not in encountered_files:
                    encountered_files.add(renamed_path)
                    self.clean_up.append((False, renamed_path))
        for path, _ in self.output_files:
            # Create directories for expected output and mark them to be cleaned up at the end
            # of the test case.
            dir = os.path.dirname(path)
            for d in self.add_dirs(dir):
                self.clean_up.append((True, d))
            self.clean_up.append((False, path))

        sys.path.insert(0, tmpdir_root)

    def teardown(self):
        if hasattr(self, 'old_environ'):
            os.environ = self.old_environ
        super().teardown()


def split_test_cases(parent: 'DataSuiteCollector', suite: 'DataSuite',
                     file: str) -> Iterator[DjangoDataDrivenTestCase]:
    """Iterate over raw test cases in file, at collection time, ignoring sub items.

    The collection phase is slow, so any heavy processing should be deferred to after
    uninteresting tests are filtered (when using -k PATTERN switch).
    """
    with open(file, encoding='utf-8') as f:
        data = f.read()
    cases = re.split(r'^\[case ([a-zA-Z_0-9]+)'
                     r'(-writescache)?'
                     r'(-only_when_cache|-only_when_nocache)?'
                     r'(-skip)?'
                     r'\][ \t]*$\n', data,
                     flags=re.DOTALL | re.MULTILINE)
    line_no = cases[0].count('\n') + 1

    for i in range(1, len(cases), 5):
        name, writescache, only_when, skip, data = cases[i:i + 5]
        yield DjangoDataDrivenTestCase(parent, suite, file,
                                       name=add_test_name_suffix(name, suite.test_name_suffix),
                                       writescache=bool(writescache),
                                       only_when=only_when,
                                       skip=bool(skip),
                                       data=data,
                                       line=line_no)
        line_no += data.count('\n') + 1


class DataSuiteCollector(pytest.Class):  # type: ignore  # inheriting from Any
    def collect(self) -> Iterator[pytest.Item]:  # type: ignore
        """Called by pytest on each of the object returned from pytest_pycollect_makeitem"""

        # obj is the object for which pytest_pycollect_makeitem returned self.
        suite = self.obj  # type: DataSuite
        for f in suite.files:
            yield from split_test_cases(self, suite, os.path.join(suite.data_prefix, f))


# This function name is special to pytest.  See
# http://doc.pytest.org/en/latest/writing_plugins.html#collection-hooks
def pytest_pycollect_makeitem(collector: Any, name: str,
                              obj: object) -> 'Optional[Any]':
    """Called by pytest on each object in modules configured in conftest.py files.

    collector is pytest.Collector, returns Optional[pytest.Class]
    """
    if isinstance(obj, type):
        # Only classes derived from DataSuite contain test cases, not the DataSuite class itself
        if issubclass(obj, DataSuite) and obj is not DataSuite:
            # Non-None result means this obj is a test case.
            # The collect method of the returned DataSuiteCollector instance will be called later,
            # with self.obj being obj.
            return DataSuiteCollector(name, parent=collector)
    return None
