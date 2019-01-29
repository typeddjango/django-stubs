import os
import re
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Pattern

from git import Repo
from mypy import build
from mypy.main import process_options

DJANGO_BRANCH = 'stable/2.1.x'
DJANGO_COMMIT_SHA = '03219b5f709dcd5b0bfacd963508625557ec1ef0'
IGNORED_ERROR_PATTERNS = [
    'Need type annotation for',
    'already defined on',
    'Cannot assign to a',
    'cannot perform relative import',
    'broken_app',
    'LazySettings',
    'Cannot infer type of lambda',
    'Incompatible types in assignment (expression has type "Callable[',
    'Invalid value for a to= parameter',
    'Incompatible types in assignment (expression has type "FilteredChildAdmin", variable has type "ChildAdmin")',
    re.compile(r'"Callable\[\[(Any(, )?)+\], Any\]" has no attribute'),
    re.compile(r'"HttpResponseBase" has no attribute "[A-Za-z_]+"'),
    re.compile(r'Incompatible types in assignment \(expression has type "Tuple\[\]", '
               r'variable has type "Tuple\[[A-Za-z, ]+\]"'),
]
TESTS_DIRS = [
    'absolute_url_overrides',
    'admin_autodiscover',
    'admin_changelist',
]


@contextmanager
def cd(path):
    """Context manager to temporarily change working directories"""
    if not path:
        return
    prev_cwd = Path.cwd().as_posix()
    if isinstance(path, Path):
        path = path.as_posix()
    os.chdir(str(path))
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def is_ignored(line: str) -> bool:
    for pattern in IGNORED_ERROR_PATTERNS:
        if isinstance(pattern, Pattern):
            if pattern.search(line):
                return True
        else:
            if pattern in line:
                return True
    return False


def check_with_mypy(abs_path: Path, config_file_path: Path) -> int:
    error_happened = False
    with cd(abs_path):
        sources, options = process_options(['--config-file', str(config_file_path), str(abs_path)])
        res = build.build(sources, options)
        for error_line in res.errors:
            if not is_ignored(error_line):
                error_happened = True
                print(error_line)
    return int(error_happened)


if __name__ == '__main__':
    project_directory = Path(__file__).parent.parent
    mypy_config_file = (project_directory / 'scripts' / 'mypy.ini').absolute()
    repo_directory = project_directory / 'django-sources'
    tests_root = repo_directory / 'tests'
    global_rc = 0

    # clone Django repository, if it does not exist
    if not repo_directory.exists():
        repo = Repo.clone_from('https://github.com/django/django.git', repo_directory)
    else:
        repo = Repo(repo_directory)
        repo.remotes['origin'].pull(DJANGO_BRANCH)

    repo.git.checkout(DJANGO_COMMIT_SHA)
    for dirname in TESTS_DIRS:
        abs_path = (project_directory / tests_root / dirname).absolute()
        print(f'Checking {abs_path.as_uri()}')

        rc = check_with_mypy(abs_path, mypy_config_file)
        if rc != 0:
            global_rc = 1

    sys.exit(rc)
