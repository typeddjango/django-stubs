import itertools
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Pattern

from scripts.enabled_test_modules import IGNORED_ERRORS, IGNORED_MODULES

PROJECT_DIRECTORY = Path(__file__).parent.parent


def is_ignored(line: str, test_folder_name: str) -> bool:
    if 'runtests' in line:
        return True

    if test_folder_name in IGNORED_MODULES:
        return True

    for pattern in itertools.chain(IGNORED_ERRORS['__new_common__'],
                                   IGNORED_ERRORS.get(test_folder_name, [])):
        if isinstance(pattern, Pattern):
            if pattern.search(line):
                return True
        else:
            if pattern in line:
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
                        '--config-file', str(mypy_config_file)]
        mypy_options += [str(tests_root)]

        import distutils.spawn

        mypy_executable = distutils.spawn.find_executable('mypy')
        mypy_argv = [mypy_executable, *mypy_options]
        completed = subprocess.run(
            mypy_argv,
            env={'PYTHONPATH': str(tests_root)},
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        rc = completed.returncode
        stdout = completed.stdout.decode()
        stderr = completed.stderr.decode()
        if rc not in (0, 1) or stderr:
            import shlex

            cmd = " ".join(shlex.quote(s) for s in mypy_argv)
            print("Failed to run {} (exitcode {})!".format(cmd, rc), file=sys.stderr)
            if stderr:
                print("=== Output on stderr: ===\n{}".format(stderr.rstrip("\n")))
            if stdout:
                print("=== Output on stdout: ===\n{}".format(stdout.rstrip("\n")))
            sys.exit(rc or 1)

        sorted_lines = sorted(stdout.splitlines())
        for line in sorted_lines:
            try:
                module_name = line.split('/')[0]
            except IndexError:
                module_name = 'unknown'

            if not is_ignored(line, module_name):
                if line.startswith(module_name):
                    print(replace_with_clickable_location(line, abs_test_folder=tests_root))
                else:
                    print(line)

        sys.exit(global_rc)

    except BaseException as exc:
        shutil.rmtree(mypy_cache_dir, ignore_errors=True)
        raise exc
