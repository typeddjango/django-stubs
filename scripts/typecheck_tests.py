import itertools
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Pattern, Union

from scripts.enabled_test_modules import (
    EXTERNAL_MODULES, IGNORED_ERRORS, IGNORED_MODULES, MOCK_OBJECTS,
)

PROJECT_DIRECTORY = Path(__file__).parent.parent


def print_unused_ignores(ignored_message_freq):
    for root_key, patterns in IGNORED_ERRORS.items():
        for pattern in patterns:
            if (ignored_message_freq[root_key][pattern] == 0
                    and pattern not in itertools.chain(EXTERNAL_MODULES, MOCK_OBJECTS)):
                print(f'{root_key}: {pattern}')


def is_pattern_fits(pattern: Union[Pattern, str], line: str):
    if isinstance(pattern, Pattern):
        if pattern.search(line):
            return True
    else:
        if pattern in line:
            return True
    return False


def is_ignored(line: str, test_folder_name: str, *, ignored_message_freqs: Dict[str, Dict[str, int]]) -> bool:
    if 'runtests' in line:
        return True

    if test_folder_name in IGNORED_MODULES:
        return True

    for pattern in IGNORED_ERRORS['__new_common__']:
        if is_pattern_fits(pattern, line):
            ignored_message_freqs['__new_common__'][pattern] += 1
            return True

    for pattern in IGNORED_ERRORS.get(test_folder_name, []):
        if is_pattern_fits(pattern, line):
            ignored_message_freqs[test_folder_name][pattern] += 1
            return True

    return False


def replace_with_clickable_location(error: str, abs_test_folder: Path) -> str:
    raw_path, _, error_line = error.partition(': ')
    fname, _, line_number = raw_path.partition(':')

    try:
        path = abs_test_folder.joinpath(fname).relative_to(PROJECT_DIRECTORY)
    except ValueError:
        # fail on travis, just show an error
        return error

    clickable_location = f'./{path}:{line_number or 1}'
    return error.replace(raw_path, clickable_location)


if __name__ == '__main__':
    mypy_config_file = (PROJECT_DIRECTORY / 'scripts' / 'mypy.ini').absolute()
    repo_directory = PROJECT_DIRECTORY / 'django-sources'
    mypy_cache_dir = Path(__file__).parent / '.mypy_cache'
    tests_root = repo_directory / 'tests'
    global_rc = 0

    try:
        mypy_options = ['--cache-dir', str(mypy_config_file.parent / '.mypy_cache'),
                        '--config-file', str(mypy_config_file),
                        '--show-traceback',
                        # '--no-error-summary',
                        # '--no-pretty',
                        '--hide-error-context'
                        ]
        mypy_options += [str(tests_root)]

        import distutils.spawn

        mypy_executable = distutils.spawn.find_executable('mypy')
        mypy_argv = [mypy_executable, *mypy_options]
        completed = subprocess.run(
            mypy_argv,
            env={'PYTHONPATH': str(tests_root)},
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        output = completed.stdout.decode()

        ignored_message_freqs = defaultdict(lambda: defaultdict(int))

        sorted_lines = sorted(output.splitlines())
        for line in sorted_lines:
            try:
                path_to_error = line.split(':')[0]
                test_folder_name = path_to_error.split('/')[2]
            except IndexError:
                test_folder_name = 'unknown'

            if not is_ignored(line, test_folder_name,
                              ignored_message_freqs=ignored_message_freqs):
                global_rc = 1
                print(line)

        print('UNUSED IGNORES ------------------------------------------------')
        print_unused_ignores(ignored_message_freqs)
        sys.exit(global_rc)

    except BaseException as exc:
        shutil.rmtree(mypy_cache_dir, ignore_errors=True)
        raise exc
