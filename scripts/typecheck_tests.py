import os
import re
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Pattern

from git import Repo
from mypy import build
from mypy.main import process_options

# Django branch to typecheck against
DJANGO_BRANCH = 'stable/2.1.x'

# Specific commit in the Django repository to check against
DJANGO_COMMIT_SHA = '03219b5f709dcd5b0bfacd963508625557ec1ef0'

# Some errors occur for the test suite itself, and cannot be addressed via django-stubs. They should be ignored
# using this constant.
IGNORED_ERROR_PATTERNS = [
    'Need type annotation for',
    'already defined on',
    'Cannot assign to a',
    'cannot perform relative import',
    'broken_app',
    'cache_clear',
    'call_count',
    'call_args_list',
    'call_args',
    '"password_changed" does not return a value',
    '"validate_password" does not return a value',
    'LazySettings',
    'Cannot infer type of lambda',
    '"refresh_from_db" of "Model"',
    '"as_sql" undefined in superclass',
    'Incompatible types in assignment (expression has type "str", target has type "type")',
    'Incompatible types in assignment (expression has type "Callable[',
    'Invalid value for a to= parameter',
    'Incompatible types in assignment (expression has type "FilteredChildAdmin", variable has type "ChildAdmin")',
    'Incompatible types in assignment (expression has type "RelatedFieldWidgetWrapper", variable has type "AdminRadioSelect")',
    'has incompatible type "MockRequest"; expected "WSGIRequest"',
    '"NullTranslations" has no attribute "_catalog"',
    re.compile(r'"Callable\[\[(Any(, )?)+\], Any\]" has no attribute'),
    re.compile(r'"HttpResponseBase" has no attribute "[A-Za-z_]+"'),
    re.compile(r'Incompatible types in assignment \(expression has type "Tuple\[\]", '
               r'variable has type "Tuple\[[A-Za-z, ]+\]"'),
    re.compile(r'"validate" of "[A-Za-z]+" does not return a value'),
    re.compile(r'Module has no attribute "[A-Za-z]+"'),
    re.compile(r'"[A-Za-z\[\]]+" has no attribute "getvalue"'),
    # TODO: remove when reassignment will be possible (in 0.670? )
    re.compile(r'Incompatible types in assignment \(expression has type "(QuerySet|List){1}\[[A-Za-z, ]+\]", '
               r'variable has type "(QuerySet|List){1}\[[A-Za-z, ]+\]"\)'),
    re.compile(r'"MockRequest" has no attribute "[a-zA-Z_]+"'),
]

# Test folders to typecheck
TESTS_DIRS = [
    'absolute_url_overrides',
    'admin_autodiscover',
    'admin_changelist',
    'admin_checks',
    'admin_custom_urls',
    'admin_default_site',
    'admin_docs',
    # TODO: 'admin_filters',
    'admin_inlines',
    'admin_ordering',
    'admin_registration',
    'admin_scripts',
    # TODO: 'admin_utils',
    # TODO: 'admin_views',
    'admin_widgets',
    'aggregation',
    'aggregation_regress',
    'annotations',
    'app_loading',
    'apps',
    # TODO: auth_tests
    'base',
    'bash_completion',
    'basic',
    'builtin_server',
    'bulk_create',
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
