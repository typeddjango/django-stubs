import os
import sys

if not os.path.exists('./django-sources'):
    git clone -b stable/2.1.x https://github.com/django/django.git django-sources

IGNORED_ERROR_PATTERNS = [
    'Need type annotation for',
    'already defined on',
    'Cannot assign to a',
    'cannot perform relative import',
    'broken_app',
    'LazySettings',
    'Cannot infer type of lambda',
    'Incompatible types in assignment (expression has type "Callable[',
    '"Callable[[Any], Any]" has no attribute',
    'Invalid value for a to= parameter'
]
TESTS_DIRS = [
    'absolute_url_overrides',
    'admin_*',
    'aggregation',
    'aggregation_regress',
    'annotations',
    'app_loading',
    'apps',
    'auth_tests'
]

def check_file_in_the_current_directory(directory, fname):
    cd @(directory)
    with ${...}.swap(FNAME=fname):
        for line in $(mypy --config-file ../../../scripts/mypy.ini $FNAME).split('\n'):
            for pattern in IGNORED_ERROR_PATTERNS:
                if pattern in line:
                    break
            else:
                if line:
                    print(line, file=sys.stderr)
    cd -

def parse_ls_output_into_fnames(output):
    fnames = []
    for line in output.splitlines()[1:]:
        fnames.append(line.split()[-1])
    return fnames

all_tests_dirs = []
for test_dir in TESTS_DIRS:
    with ${...}.swap(TEST_DIR=test_dir):
        dirs = g`django-sources/tests/$TEST_DIR`
        all_tests_dirs.extend(dirs)

for tests_dir in all_tests_dirs:
    print('Checking ' + tests_dir)
    abs_dir = os.path.join(os.getcwd(), tests_dir)

    with ${...}.swap(ABS_DIR=abs_dir):
        ls_output = $(ls -lhv --color=auto -F --group-directories-first $ABS_DIR)
        for fname in parse_ls_output_into_fnames(ls_output):
            path_to_check = os.path.join(abs_dir, fname)
            check_file_in_the_current_directory(abs_dir, fname)

