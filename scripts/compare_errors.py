#! /usr/bin/env python3

import difflib
import json
import os
import re
import shutil
import sys
from argparse import ArgumentParser
from collections import defaultdict
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from typing import Dict, Generator, List, Set

import reapply_types
from mypy.api import run

if sys.version_info < (3, 8):
    from typing_extensions import TypedDict
else:
    from typing import TypedDict


CURRENT_DIR = (Path(__file__) / ".." / "..").resolve()
ERRORS_FILE = CURRENT_DIR / ".custom_cache" / ".apply_errors"
TEMP_ERRORS_FILE = CURRENT_DIR / ".custom_cache" / ".apply_errors_temp"

ERRORS_FILE.parent.mkdir(parents=True, exist_ok=True)
TEMP_ERRORS_FILE.parent.mkdir(parents=True, exist_ok=True)


def build_mypy_errors_cache(output: str) -> Dict[str, List[int]]:
    cache: defaultdict[str, List[int]] = defaultdict(lambda: [])
    row_regex = re.compile(r"(?P<file>[^:]+):(?P<line>\d+):(?P<description>.*)")
    for row in output:
        if "note:" in row:
            continue
        file, line, description = row_regex.match(row).groups()
        cache[f"{file}:.:{description}"].append(int(line))
    return cache


def compare_mypy_errors_caches(
    new_cache: Dict[str, List[int]],
    old_cache: Dict[str, List[int]],
) -> Generator[str, None, bool]:
    is_error = False

    new_cache_keys = set(new_cache)
    old_cache_keys = set(old_cache)

    removed = old_cache_keys - new_cache_keys
    if removed:
        yield "Mypy errors removed:"
        for key in removed:
            yield from (key.replace(":.:", f":{d}:") for d in old_cache[key])

    marker_sent = False
    for key, lines in new_cache.items():
        old = set(old_cache[key])
        new = set(lines)
        old, new = old - new, new - old
        if len(old) != len(new):
            if not marker_sent:
                yield "Mypy errors changed:"
                marker_sent = True
            yield from difflib.ndiff(
                [key.replace(":.:", f":{d}:") for d in old],
                [key.replace(":.:", f":{d}:") for d in new],
            )
            if len(old) < len(new):
                is_error = True

    return is_error


def compare_apply_errors_caches(
    new_cache: Set[str],
    old_cache: Set[str],
) -> Generator[str, None, bool]:
    removed = old_cache - new_cache
    if removed:
        yield "Reapply errors removed:"
        yield from removed

    added = new_cache - old_cache
    if added:
        yield "New reapply errors:"
        yield from added
        return True
    return False


class MetaDict(TypedDict):
    apply_errors_count: int
    mypy_errors_count: int
    apply_stdout: List[str]
    mypy_stdout: List[str]


def make_meta() -> MetaDict:
    parser = reapply_types.make_parser()
    args = parser.parse_args(["--ignore-errors", "decorators", "--no-color"])
    stdout = StringIO()
    with redirect_stdout(stdout):
        error_count, temp_dir = reapply_types.main(args)
    stdout.seek(0)

    try:
        os.chdir(temp_dir / "..")
        errors, fatal, code = run(["-p", "django", "--config-file", str((CURRENT_DIR / "mypy.ini").resolve())])
    finally:
        shutil.rmtree(temp_dir)

    try:
        mypy_errors_count = int(
            re.search(
                r"Found (\d+) errors in \d+ files \(checked \d+ source files\)",
                errors.splitlines()[-1],
            ).group(1)
        )
    except AttributeError:
        print(errors, fatal)
        sys.exit(1)

    return {
        "apply_errors_count": error_count,
        "mypy_errors_count": mypy_errors_count,
        "apply_stdout": stdout.readlines(),
        "mypy_stdout": errors.splitlines()[:-1],
    }


def compare(meta: MetaDict, old_meta: MetaDict) -> int:
    exit_code = 0

    new_apply_errors_cache = set(meta["apply_stdout"])
    old_apply_errors_cache = set(old_meta["apply_stdout"])
    diff_errors = compare_apply_errors_caches(new_apply_errors_cache, old_apply_errors_cache)

    while True:
        try:
            print(next(diff_errors).strip("\n"))
        except StopIteration as exc:
            if exc.value:
                print("Incompatible stub code was added.")
                exit_code = 2
            break

    new_mypy_errors_cache = build_mypy_errors_cache(meta["mypy_stdout"])
    old_mypy_errors_cache = build_mypy_errors_cache(old_meta["mypy_stdout"])
    diff_errors = compare_mypy_errors_caches(new_mypy_errors_cache, old_mypy_errors_cache)

    while True:
        try:
            print(next(diff_errors).strip("\n"))
        except StopIteration as exc:
            if exc.value:
                print("New type errors were introduced.")
                exit_code = max(1, exit_code)
            break

    return exit_code


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--check-only")
    args = parser.parse_args()

    sys.path.insert(0, str(CURRENT_DIR))
    meta = make_meta()

    if args.check_only:
        print("Incompatible stub code:")
        print(*meta["apply_stdout"], sep="\n")
        print("=" * 60)
        print("Mypy errors:")
        print(*meta["mypy_stdout"])
        sys.exit(0)

    with open(ERRORS_FILE) as meta_file:
        old_meta = json.load(meta_file)

    with open(TEMP_ERRORS_FILE, "w") as meta_file:
        json.dump(meta, meta_file)

    sys.exit(compare(meta, old_meta))
