import itertools
import shutil
import subprocess
import sys
from argparse import ArgumentParser
from collections import defaultdict
from distutils import spawn
from typing import Dict, List, Pattern, Union

from scripts.enabled_test_modules import EXTERNAL_MODULES, IGNORED_ERRORS, IGNORED_MODULES, MOCK_OBJECTS
from scripts.git_helpers import checkout_django_branch
from scripts.paths import DJANGO_SOURCE_DIRECTORY, PROJECT_DIRECTORY

DJANGO_COMMIT_REFS: Dict[str, str] = {
    "2.2": "8093aaa8ff9dd7386a069c6eb49fcc1c5980c033",
    "3.0": "44da7abda848f05caaed74f6a749038c87dedfda",
}


def get_unused_ignores(ignored_message_freq: Dict[str, Dict[Union[str, Pattern], int]]) -> List[str]:
    unused_ignores = []
    for root_key, patterns in IGNORED_ERRORS.items():
        for pattern in patterns:
            if ignored_message_freq[root_key][pattern] == 0 and pattern not in itertools.chain(
                EXTERNAL_MODULES, MOCK_OBJECTS
            ):
                unused_ignores.append(f"{root_key}: {pattern}")
    return unused_ignores


def is_pattern_fits(pattern: Union[Pattern, str], line: str):
    if isinstance(pattern, Pattern):
        if pattern.search(line):
            return True
    else:
        if pattern in line:
            return True
    return False


def is_ignored(line: str, test_folder_name: str, *, ignored_message_freqs: Dict[str, Dict[str, int]]) -> bool:
    if "runtests" in line:
        return True

    if test_folder_name in IGNORED_MODULES:
        return True

    for pattern in IGNORED_ERRORS.get(test_folder_name, []):
        if is_pattern_fits(pattern, line):
            ignored_message_freqs[test_folder_name][pattern] += 1
            return True

    for pattern in IGNORED_ERRORS["__common__"]:
        if is_pattern_fits(pattern, line):
            ignored_message_freqs["__common__"][pattern] += 1
            return True

    return False


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--django_version", default="3.0")
    django_version = parser.parse_args().django_version
    subprocess.check_call([sys.executable, "-m", "pip", "install", f"Django=={django_version}.*"])
    commit_sha = DJANGO_COMMIT_REFS[django_version]
    repo = checkout_django_branch(django_version, commit_sha)
    mypy_config_file = (PROJECT_DIRECTORY / "mypy.ini").absolute()
    mypy_cache_dir = PROJECT_DIRECTORY / ".mypy_cache"
    tests_root = DJANGO_SOURCE_DIRECTORY / "tests"
    global_rc = 0

    try:
        mypy_options = [
            "--cache-dir",
            str(mypy_cache_dir),
            "--config-file",
            str(mypy_config_file),
            "--show-traceback",
            "--no-error-summary",
            "--hide-error-context",
        ]
        mypy_options += [str(tests_root)]
        mypy_executable = spawn.find_executable("mypy")
        mypy_argv = [mypy_executable, *mypy_options]
        completed = subprocess.run(
            mypy_argv,
            env={"PYTHONPATH": str(tests_root), "TYPECHECK_TESTS": "1"},
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        output = completed.stdout.decode()

        ignored_message_freqs = defaultdict(lambda: defaultdict(int))

        sorted_lines = sorted(output.splitlines())
        for line in sorted_lines:
            try:
                path_to_error = line.split(":")[0]
                test_folder_name = path_to_error.split("/")[2]
            except IndexError:
                test_folder_name = "unknown"

            if not is_ignored(line, test_folder_name, ignored_message_freqs=ignored_message_freqs):
                global_rc = 1
                print(line)

        unused_ignores = get_unused_ignores(ignored_message_freqs)
        if unused_ignores:
            print("UNUSED IGNORES ------------------------------------------------")
            print("\n".join(unused_ignores))

        sys.exit(global_rc)

    except BaseException as exc:
        shutil.rmtree(mypy_cache_dir, ignore_errors=True)
        raise exc
