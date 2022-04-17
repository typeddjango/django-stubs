#! /usr/bin/env python3
import ast
import collections.abc
import contextlib
import os
import tempfile
import typing
from argparse import ArgumentParser, Namespace
from functools import singledispatchmethod
from itertools import zip_longest
from operator import attrgetter
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Iterable, Iterator, List, Optional, Set, Tuple, Union, cast

if TYPE_CHECKING:
    import black
    import colorama  # noqa: F401
    import isort
    from termcolor import colored


_ContainerT = Union[ast.Module, ast.AsyncFunctionDef, ast.FunctionDef, ast.ClassDef, ast.If, ast.Try]
_ContainerTypes = (ast.Module, ast.AsyncFunctionDef, ast.FunctionDef, ast.ClassDef, ast.If, ast.Try)


class Retyper:
    formats = {
        "method": ("Method not found: {func}", "white", "on_magenta"),
        "missing_class": ("Class not found: {name}", "red", "on_green"),
        "bases": ("Incompatible bases: {cls}", "cyan", None),
        "assignment": ("Incompatible assignment: {func}", "magenta", None),
        "wrong_kind": ("Incompatible method/attribute: {func}", "white", "on_blue"),
        "decorators": ("Incompatible decorators: {func}", "yellow", None),
        "signature": ("Incompatible signature: {func}", "red", None),
        "multi_assignment": ("Multi-target assignment not supported: : {targets}", "green", None),
        "error": ("Internal error: {src}", "white", "on_red"),
    }

    DJANGO_DECORATORS = {
        "cached_property": "property",
    }

    def __init__(
        self,
        file: Path,
        stub_file: Path,
        rel_file: str,
        ignored_decorators: Optional[Iterable[str]] = None,
        ignored_errors: Optional[Iterable[str]] = None,
        colored_output: bool = True,
        use_isort: bool = True,
        use_black: bool = False,
        for_django: bool = False,
    ) -> None:
        self.source_file, self.stub_file = file, stub_file
        self.ignored_decorators = set(ignored_decorators or [])
        self.ignored_errors = set(ignored_errors or [])
        self.colored_output = colored_output
        self.use_isort, self.use_black = use_isort, use_black
        self.django = for_django
        self.rel_file = str(rel_file)

        with open(file) as src:
            self.source = ast.parse(src.read(), file.name)
        with open(stub_file) as stubs:
            self.stub = ast.parse(stubs.read(), stub_file.name)

        for node in ast.iter_child_nodes(self.source):
            node.parent = self.source  # type: ignore[attr-defined]
            self.set_parent(node)

        self.source_cache = self.build_source_cache()
        self.mute = False
        self.errors_count = 0

    def set_parent(self, node: ast.AST) -> None:
        for child in ast.iter_child_nodes(node):
            child.parent = node  # type: ignore[attr-defined]
            self.set_parent(child)

    def build_source_cache(self) -> Dict[Union[str, Tuple[str, str]], ast.AST]:
        cache: Dict[Union[str, Tuple[str, str]], ast.AST] = {}
        self._add_to_cache(cache, self.source)
        return cache

    def _add_to_cache(
        self,
        cache: Dict[Union[str, Tuple[str, str]], ast.AST],
        node: ast.AST,
        prefix: str = "",
    ) -> None:
        _hash = self.get_hash(node)
        if isinstance(node, (ast.Module, ast.ClassDef)):
            key = f"{prefix}.{_hash}" if prefix else _hash
            for child in node.body:
                self._add_to_cache(cache, child, key or "")
            if isinstance(node, ast.ClassDef):
                cache.setdefault(key, node)
        elif _hash:
            cache.setdefault((prefix, _hash), node)

    def get_hash(self, node: ast.AST) -> str:
        result = ""

        if isinstance(node, ast.Module):
            return ""

        if isinstance(node, ast.Call):
            node = node.func

        if hasattr(node, "name"):
            result = node.name  # type: ignore[attr-defined]
        elif hasattr(node, "id"):
            result = node.id  # type: ignore[attr-defined]
        elif hasattr(node, "attr"):
            result = node.attr  # type: ignore[attr-defined]
        elif hasattr(node, "targets"):
            result = ";".join(filter(lambda el: el is not None, map(self.get_hash, node.targets)))  # type: ignore[attr-defined]
        elif hasattr(node, "target"):
            result = self.get_hash(node.target)  # type: ignore[attr-defined]
        elif hasattr(node, "value"):
            result = self.get_hash(node.value)  # type: ignore[attr-defined]

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and "setter" in self.prepare_decorators(node):
            result += "/setter"

        return result

    def log(self, reason: str, **attrs: Any) -> None:
        if self.mute or reason in self.ignored_errors:
            return

        self.errors_count += 1

        message, fore, back = self.formats[reason]
        message = f"[{self.rel_file}] " + message.format(**attrs)
        if self.colored_output:
            print(colored(message, fore, back))
        else:
            print(message)

    def is_inserted(self, node: ast.AST) -> bool:
        if getattr(node, "is_inserted", False):
            return True

        while hasattr(node, "parent"):
            node = node.parent  # type: ignore[attr-defined]
            if getattr(node, "is_inserted", False):
                return True

        return False

    def apply(self, node: Optional[ast.ClassDef] = None, prefix: str = "") -> int:
        for subnode in (node or self.stub).body:
            if not self.is_inserted(subnode) or isinstance(subnode, ast.AnnAssign):
                self._apply(subnode, prefix)
        return self.errors_count

    @singledispatchmethod
    def _apply(self, node: ast.AST, prefix: str = "") -> None:
        pass

    @_apply.register(ast.FunctionDef)
    @_apply.register(ast.AsyncFunctionDef)
    def _apply_func(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef], prefix: str = "") -> None:
        _hash = self.get_hash(node)
        try:
            orig = self.source_cache[(prefix, _hash)]
        except KeyError:
            if self.has_decorator(node, "type_check_only"):
                orig = self.source_cache.get(prefix, self.source)
                assert isinstance(orig, _ContainerTypes)
                self.append_after_imports(node, orig)
            else:
                self.log("method", func=_hash if not prefix else f"{prefix}.{_hash}")
        else:
            self.write_types(orig, node)

    @_apply.register(ast.Import)
    @_apply.register(ast.ImportFrom)
    @_apply.register(ast.If)
    @_apply.register(ast.Try)
    def _apply_import(self, node: Union[ast.Import, ast.ImportFrom, ast.If, ast.Try], prefix: str = "") -> None:
        if not prefix:
            self.append_after_imports(node)

    @_apply.register(ast.Assign)
    @_apply.register(ast.AnnAssign)
    def _apply_assign(self, node: Union[ast.Assign, ast.AnnAssign], prefix: str = "") -> None:
        _hash = self.get_hash(node)

        if isinstance(node, ast.AnnAssign) and isinstance(node.value, ast.Constant) and node.value.value is Ellipsis:
            del node.value

        try:
            orig = self.source_cache[(prefix, _hash)]
        except KeyError:
            if not prefix:
                root: _ContainerT = self.source
            else:
                _root = self.source_cache[prefix]
                assert isinstance(_root, _ContainerTypes)
                root = _root
            self.write_types(None, node, root)
        else:
            self.write_types(orig, node)

    @_apply.register
    def _apply_class(self, node: ast.ClassDef, prefix: str = "") -> None:
        _hash = self.get_hash(node)
        if prefix:
            _hash = f"{prefix}.{_hash}"

        if _hash not in self.source_cache:
            if not self.has_decorator(node, "type_check_only"):
                self.log("missing_class", name=_hash)
            base = self.source_cache.get(prefix, self.source)
            assert isinstance(base, _ContainerTypes)
            self.append_after_imports(node, base)
            self._add_to_cache(self.source_cache, node, prefix)
            self.apply(node, _hash)
        else:
            src = self.source_cache[_hash]
            if self.incompatible_bases(cast(ast.ClassDef, src), node):
                self.log("bases", cls=node.name)

            self.apply(node, _hash)

    @contextlib.contextmanager
    def disable_logging(self) -> Iterator[None]:
        self.mute = True
        yield
        self.mute = False

    def incompatible_bases(self, src: ast.ClassDef, node: ast.ClassDef) -> bool:
        node_bases_dumps = [ast.dump(b) for b in node.bases]
        src_bases_dumps = [ast.dump(b) for b in src.bases]
        if node_bases_dumps == src_bases_dumps:
            return False

        src_bases = [self.get_hash(b) for b in src.bases]

        for base in node.bases:
            if ast.dump(base) in src_bases_dumps:
                continue
            cls = base.value if isinstance(base, ast.Subscript) else base
            _hash = self.get_hash(cls)
            if getattr(typing, _hash, None) is not None:
                src.bases.append(base)

                # Exclude most common bases which can be duplicated
                # and keep only the one from `typing`
                if _hash.lower() in {"list", "tuple", "dict", "set", "frozenset"} and _hash.lower() in src_bases:
                    del src.bases[src_bases.index(_hash.lower())]
                elif getattr(collections.abc, _hash, None) is not None and _hash in src_bases:
                    del src.bases[src_bases.index(_hash)]
            elif _hash in src_bases:
                where = src_bases.index(_hash)
                src.bases[where] = base
        return {ast.dump(b) for b in src.bases} != {ast.dump(b) for b in node.bases}

    @singledispatchmethod
    def write_types(self, orig: ast.AST, stub: ast.AST, root: Optional[_ContainerT] = None) -> None:
        pass

    @write_types.register(ast.FunctionDef)
    @write_types.register(ast.AsyncFunctionDef)
    def write_types_func(
        self,
        orig: Union[ast.FunctionDef, ast.AsyncFunctionDef],
        stub: ast.AST,
        root: Optional[ast.AST] = None,
    ) -> None:
        _hash = self.get_hash(orig)
        prefix = getattr(getattr(orig, "parent", None), "name", "")
        func = _hash if not prefix else f"{prefix}.{_hash}"

        if not isinstance(stub, (ast.FunctionDef, ast.AsyncFunctionDef)):
            self.log("wrong_kind", func=func)
            return

        if self.has_decorator(stub, "overload"):
            self.insert_before(orig, stub)
            return

        if self.prepare_decorators(stub) != self.prepare_decorators(orig):
            self.log("decorators", func=func)

        if self.django:
            for i, dec in enumerate(orig.decorator_list):
                if (decorator_name := self.extract_decorator(dec)) is None:
                    continue
                if new := self.DJANGO_DECORATORS.get(decorator_name):
                    orig.decorator_list[i] = ast.Name(id=new, ctx=ast.Load())

        stub_args = self.get_func_args(stub)
        orig_args = self.get_func_args(orig)

        def flatten(args_dict: Dict[str, Tuple[ast.arg, bool]]) -> Dict[str, bool]:
            return {name: has_default for name, (_, has_default) in args_dict.items()}

        if flatten(stub_args) != flatten(orig_args):
            self.log("signature", func=func)

        for arg_name, (arg, _) in orig_args.items():
            with contextlib.suppress(KeyError):
                arg.annotation = stub_args.pop(arg_name)[0].annotation
        orig.returns = stub.returns

    def get_func_args(self, func: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> Dict[str, Tuple[ast.arg, bool]]:
        st = func.args
        return (
            {a.arg: (a, False) for a in st.posonlyargs}
            | {a.arg: (a, d is not None) for a, d in zip_longest(reversed(st.args), reversed(st.defaults))}
            | {a.arg: (a, d is not None) for a, d in zip_longest(reversed(st.kwonlyargs), reversed(st.kw_defaults))}
            | ({st.vararg.arg: (st.vararg, False)} if st.vararg else {})
            | ({st.kwarg.arg: (st.kwarg, False)} if st.kwarg else {})
        )

    def _are_same(self, node1: ast.AST, node2: ast.AST) -> bool:
        # It can be slow for large nodes, but we need it only for simple cases
        return type(node1) is type(node2) and ast.dump(node1) == ast.dump(node2)  # noqa: E721

    @write_types.register
    def write_types_assign(self, orig: ast.Assign, stub: ast.AST, root: Optional[_ContainerT] = None) -> None:
        if not isinstance(stub, ast.AnnAssign):
            if not self._are_same(orig, stub):
                if isinstance(stub, ast.Assign):
                    self.log("assignment", func=self.get_hash(stub))
                else:
                    self.log("wrong_kind", func=self.get_hash(stub))
            return
        if len(orig.targets) != 1:
            self.log(
                "multi_assignment",
                targets=" = ".join(map(attrgetter("id"), orig.targets)),
            )
            return

        try:
            where = orig.parent.body.index(orig)  # type: ignore[attr-defined]
        except ValueError:
            self.log("error", src=f"{self.get_hash(orig.parent)}.{self.get_hash(orig)}")  # type: ignore[attr-defined]  # noqa: E501
            return

        new_node = ast.AnnAssign(
            target=orig.targets[0],
            value=orig.value,
            annotation=stub.annotation,
            simple=1,
        )
        ast.copy_location(new_node, orig)
        orig.parent.body[where] = new_node  # type: ignore[attr-defined]

    @write_types.register
    def write_types_annassign(
        self, orig: ast.AnnAssign, stub: ast.AnnAssign, root: Optional[_ContainerT] = None
    ) -> None:
        can_clear = isinstance(orig.value, ast.Constant) and orig.value.value is Ellipsis and self.is_inserted(orig)

        if can_clear:
            del orig.value

    @write_types.register
    def write_types_add_new(self, orig: None, stub: ast.AnnAssign, root: Optional[_ContainerT] = None) -> None:
        self.append_after_imports(stub, root)

    def extract_decorator(self, d: ast.AST) -> Optional[str]:
        if isinstance(d, ast.Call):
            d = d.func

        if isinstance(d, ast.Name):
            return d.id
        return getattr(d, "attr", None)

    def prepare_decorators(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef]) -> Set[str]:
        decorators = {self.extract_decorator(d): d for d in node.decorator_list}
        return cast(Set[str], set(decorators) - self.ignored_decorators - {None})

    def append_after_imports(self, stub: ast.AST, root: Optional[_ContainerT] = None) -> None:
        if root is None:
            root = self.source

        stub.is_inserted = True  # type: ignore[attr-defined]
        for i, child in enumerate(root.body):
            if (
                not isinstance(child, (ast.Import, ast.ImportFrom))
                and (
                    i != 0
                    or not isinstance(child, ast.Expr)
                    or not isinstance(getattr(child, "value", None), ast.Constant)
                )
                and not getattr(child, "is_inserted", False)
            ):
                break
        else:
            cast(List[ast.AST], root.body).insert(-1, stub)
            return

        child.parent = root  # type: ignore[attr-defined]
        self.insert_before(child, stub)

    def has_decorator(
        self,
        node: Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef],
        name: str,
    ) -> bool:
        return any(d == name for d in self.prepare_decorators(node))

    def insert_before(self, ref_node: ast.AST, new_node: ast.AST) -> None:
        height = cast(int, new_node.end_lineno) - new_node.lineno + 1
        new_node.lineno = ref_node.lineno
        new_node.col_offset = ref_node.col_offset
        new_node.inserted = True  # type: ignore[attr-defined]

        siblings = ref_node.parent.body  # type: ignore[attr-defined]
        where = siblings.index(ref_node)
        siblings.insert(where, new_node)

        new_node.parent = ref_node.parent  # type: ignore[attr-defined]
        self.set_parent(new_node)

        ast.increment_lineno(ref_node, height)

    def insert_after(self, ref_node: ast.AST, new_node: ast.AST) -> None:
        height = cast(int, new_node.end_lineno) - new_node.lineno
        new_node.lineno = cast(int, ref_node.end_lineno) + 1
        new_node.col_offset = ref_node.col_offset
        new_node.inserted = True  # type: ignore[attr-defined]

        siblings = ref_node.parent.body  # type: ignore[attr-defined]
        where = siblings.index(ref_node)
        siblings.insert(where + 1, new_node)

        new_node.parent = ref_node.parent  # type: ignore[attr-defined]
        self.set_parent(new_node)

        with contextlib.suppress(IndexError):
            ast.increment_lineno(siblings[where + 2], height)

    def write(self, target: Path) -> None:
        code = ast.unparse(self.source)

        if self.use_isort:
            code = isort.code(code)
        if self.use_black:
            code = black.format_str(code, mode=black.FileMode())

        with open(target, "w") as file:
            file.write(code)


def make_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="Apply annotations from stub files to source",
    )
    try:
        import django
    except ImportError:
        parser.add_argument(
            "source",
            type=Path,
            help="Source files directory",
        )
    else:
        parser.add_argument(
            "source",
            type=Path,
            help="Source files directory",
            default=(Path(django.__file__) / "..").resolve(),
            nargs="?",
        )
    parser.add_argument(
        "stub",
        type=Path,
        help="Stub files directory",
        nargs="?",
        default=(Path(__file__) / ".." / ".." / "django-stubs").resolve(),
    )
    parser.add_argument(
        "target",
        type=Path,
        help="Output files directory (will be overwritten)",
        default=Path(tempfile.mkdtemp()),
        nargs="?",
    )
    parser.add_argument(
        "--ignore-decorators",
        action="extend",
        nargs="+",
        default=[],
        help="Decorators to exclude from checks (only function name, like `lru_cache`)",
    )
    parser.add_argument(
        "--ignore-errors",
        action="extend",
        nargs="+",
        default=[],
        choices=[*Retyper.formats, "missing_source"],
        help="Error types to ignore",
    )
    parser.add_argument(
        "--no-color",
        action="store_false",
        dest="color",
        default=True,
        help="Disable output coloring",
    )
    parser.add_argument(
        "--no-isort",
        action="store_false",
        dest="isort",
        default=True,
        help="Disable output ",
    )
    parser.add_argument(
        "--black",
        action="store_true",
        default=False,
        help="Format output with black",
    )
    parser.add_argument(
        "--django",
        action="store_true",
        default=False,
        help="Perform django-specific tasks",
    )
    return parser


def main(args: Namespace) -> Tuple[int, Path]:
    global colorama, colored, isort, black
    if args.color:
        try:
            import colorama
        except ImportError:
            args.color = False
            print(
                "Package colorama is not installed. Disabling input coloring. "
                "Use --no-color to silence this warning."
            )
        else:
            colorama.init()

        try:
            from termcolor import colored
        except ImportError:
            args.color = False
            print(
                "Package termcolor is not installed. Disabling input coloring. "
                "Use --no-color to silence this warning."
            )
    if args.isort:
        try:
            import isort
        except ImportError:
            args.isort = False
            print("Package isort is not installed. " "Use --no-isort to silence this warning.")
    if args.black:
        try:
            import black
        except ImportError:
            args.black = False
            print("Package black is not installed. " "Don't use --black to silence this warning.")

    args.target /= "django"
    errors = 0
    for full_path in args.stub.rglob("*.pyi"):
        rel_path = os.path.relpath(full_path, args.stub)
        try:
            retyper = Retyper(
                args.source / rel_path[:-1],
                args.stub / rel_path,
                "django/" + rel_path,
                args.ignore_decorators,
                args.ignore_errors,
                args.color,
                args.isort,
                args.black,
                args.django,
            )
        except FileNotFoundError:
            if "missing_source" not in args.ignore_errors:
                message = f"[{rel_path}] Source not found"
                if args.color:
                    print(colored(message, "white", "on_red"))
                else:
                    print(message)
            continue

        errors += retyper.apply()
        target_dir = (args.target / rel_path / "..").resolve()
        target_dir.mkdir(parents=True, exist_ok=True)
        retyper.write(args.target / rel_path[:-1])

    return errors, args.target


if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()
    main(args)
