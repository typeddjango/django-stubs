import os
import re
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Pattern

from git import Repo
from mypy import build
from mypy.main import process_options

PROJECT_DIRECTORY = Path(__file__).parent.parent

# Django branch to typecheck against
DJANGO_BRANCH = 'stable/2.1.x'

# Specific commit in the Django repository to check against
DJANGO_COMMIT_SHA = '03219b5f709dcd5b0bfacd963508625557ec1ef0'

# Some errors occur for the test suite itself, and cannot be addressed via django-stubs. They should be ignored
# using this constant.
MOCK_OBJECTS = ['MockRequest', 'MockCompiler', 'modelz']
IGNORED_ERRORS = {
    '__common__': [
        *MOCK_OBJECTS,
        'LazySettings',
        'NullTranslations',
        'Need type annotation for',
        'Invalid value for a to= parameter',
        'already defined (possibly by an import)',
        'Cannot assign to a type',
        # forms <-> models plugin support
        '"Model" has no attribute',
        re.compile(r'Cannot determine type of \'(objects|stuff)\''),
        # settings
        re.compile(r'Module has no attribute "[A-Z_]+"'),
        # attributes assigned to test functions
        re.compile(r'"Callable\[\[(Any(, )?)+\], Any\]" has no attribute'),
        # assign empty tuple
        re.compile(r'Incompatible types in assignment \(expression has type "Tuple\[\]", '
                   r'variable has type "Tuple\[[A-Za-z, ]+\]"'),
        # assign method to a method
        'Cannot assign to a method',
        'Cannot infer type of lambda',
        re.compile(r'Incompatible types in assignment \(expression has type "Callable\[\[(Any(, )?)+\], Any\]", '
                   r'variable has type "Callable\['),
    ],
    'admin_changelist': [
        'Incompatible types in assignment (expression has type "FilteredChildAdmin", variable has type "ChildAdmin")'
    ],
    'admin_scripts': [
        'Incompatible types in assignment (expression has type "Callable['
    ],
    'admin_widgets': [
        'Incompatible types in assignment (expression has type "RelatedFieldWidgetWrapper", '
        'variable has type "AdminRadioSelect")',
        'Incompatible types in assignment (expression has type "Widget", variable has type "AutocompleteSelect")'
    ],
    'aggregation': [
        'Incompatible types in assignment (expression has type "QuerySet[Any]", variable has type "List[Any]")',
        '"as_sql" undefined in superclass'
    ],
    'aggregation_regress': [
        'Incompatible types in assignment (expression has type "List[str]", variable has type "QuerySet[Author]")'
    ],
    'basic': [
        'Unexpected keyword argument "unknown_kwarg" for "refresh_from_db" of "Model"',
        '"refresh_from_db" of "Model" defined here'
    ],
    'builtin_server': [
        'has no attribute "getvalue"'
    ],
    'csrf_tests': [
        'Incompatible types in assignment (expression has type "property", ' +
        'base class "HttpRequest" defined the type as "QueryDict")'
    ],
    'dates': [
        'Too few arguments for "dates" of "QuerySet"',
    ],
    'defer': [
        'Too many arguments for "refresh_from_db" of "Model"'
    ],
    'db_typecasts': [
        '"object" has no attribute "__iter__"; maybe "__str__" or "__dir__"? (not iterable)'
    ],
    'from_db_value': [
        'has no attribute "vendor"'
    ],
    'get_object_or_404': [
        'Argument 1 to "get_object_or_404" has incompatible type "str"; '
        + 'expected "Union[Type[Model], Manager[Any], QuerySet[Any]]"',
        'Argument 1 to "get_object_or_404" has incompatible type "Type[CustomClass]"; '
        + 'expected "Union[Type[Model], Manager[Any], QuerySet[Any]]"',
        'Argument 1 to "get_list_or_404" has incompatible type "List[Type[Article]]"; '
        + 'expected "Union[Type[Model], Manager[Any], QuerySet[Any]]"'
    ],
    'model_inheritance_regress': [
        'Incompatible types in assignment (expression has type "List[Supplier]", variable has type "QuerySet[Supplier]")'
    ],
    'model_meta': [
        '"object" has no attribute "items"',
        '"Field" has no attribute "many_to_many"'
    ],
    'migrate_signals': [
        'Value of type "None" is not indexable',
    ],
    'queryset_pickle': [
        '"None" has no attribute "somefield"'
    ],
    'prefetch_related': [
        'Incompatible types in assignment (expression has type "List[Room]", variable has type "QuerySet[Room]")',
        '"None" has no attribute "__iter__"',
        'has no attribute "read_by"'
    ],
    'urlpatterns': [
        '"object" has no attribute "__iter__"; maybe "__str__" or "__dir__"? (not iterable)',
        '"object" not callable'
    ],
    'user_commands': [
        'Incompatible types in assignment (expression has type "Callable[[Any, KwArg(Any)], Any]", variable has type'
    ],
    'sessions_tests': [
        'base class "SessionTestsMixin" defined the type as "None")',
        'has no attribute "_reserved"'
    ],
    'select_related_onetoone': [
        '"None" has no attribute'
    ]
}
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
    # TODO: 'apps',
    # TODO: 'auth_tests'
    'base',
    'bash_completion',
    'basic',
    'builtin_server',
    'bulk_create',
    # TODO: 'cache',
    # TODO: 'check_framework',
    'choices',
    'conditional_processing',
    # TODO: 'contenttypes_tests',
    'context_processors',
    'csrf_tests',
    'custom_columns',
    # TODO: 'custom_lookups',
    # TODO: 'custom_managers',
    'custom_methods',
    'custom_migration_operations',
    'custom_pk',
    'datatypes',
    'dates',
    'datetimes',
    'db_functions',
    'db_typecasts',
    'db_utils',
    'dbshell',
    # TODO: 'decorators',
    'defer',
    # TODO: 'defer_regress',
    'delete',
    'delete_regress',
    # TODO: 'deprecation',
    # TODO: 'dispatch',
    'distinct_on_fields',
    'empty',
    # TODO: 'expressions',
    'expressions_case',
    # TODO: 'expressions_window',
    # TODO: 'extra_regress',
    # TODO: 'field_deconstruction',
    'field_defaults',
    'field_subclassing',
    # TODO: 'file_storage',
    # TODO: 'file_uploads',
    # TODO: 'files',
    'filtered_relation',
    # TODO: 'fixtures',
    'fixtures_model_package',
    # TODO: 'fixtures_regress',
    # TODO: 'flatpages_tests',
    'force_insert_update',
    'foreign_object',
    # TODO: 'forms_tests',
    'from_db_value',
    # TODO: 'generic_inline_admin',
    # TODO: 'generic_relations',
    'generic_relations_regress',
    # TODO: 'generic_views',
    'get_earliest_or_latest',
    'get_object_or_404',
    # TODO: 'get_or_create',
    # TODO: 'gis_tests',
    'handlers',
    # TODO: 'httpwrappers',
    'humanize_tests',
    # TODO: 'i18n',
    'import_error_package',
    'indexes',
    'inline_formsets',
    'inspectdb',
    'introspection',
    # TODO: 'invalid_models_tests',
    'known_related_objects',
    # TODO: 'logging_tests',
    # TODO: 'lookup',
    'm2m_and_m2o',
    'm2m_intermediary',
    'm2m_multiple',
    'm2m_recursive',
    'm2m_regress',
    'm2m_signals',
    'm2m_through',
    'm2m_through_regress',
    'm2o_recursive',
    # TODO: 'mail',
    'managers_regress',
    'many_to_many',
    'many_to_one',
    'many_to_one_null',
    'max_lengths',
    # TODO: 'messages_tests',
    # TODO: 'middleware',
    # TODO: 'middleware_exceptions',
    'migrate_signals',
    'migration_test_data_persistence',
    # TODO: 'migrations',
    'migrations2',
    # TODO: 'model_fields',
    # TODO: 'model_forms',
    'model_formsets',
    'model_formsets_regress',
    'model_indexes',
    # TODO: 'model_inheritance',
    'model_inheritance_regress',
    'model_meta',
    'model_options',
    'model_package',
    'model_regress',
    # TODO: 'modeladmin',
    # TODO: 'multiple_database',
    'mutually_referential',
    'nested_foreign_keys',
    'no_models',
    'null_fk',
    'null_fk_ordering',
    'null_queries',
    'one_to_one',
    'or_lookups',
    'order_with_respect_to',
    'ordering',
    'prefetch_related',
    'pagination',
    # TODO: 'postgres_tests',
    'project_template',
    'properties',
    'proxy_model_inheritance',
    # TODO: 'proxy_models',
    # TODO: 'queries',
    'queryset_pickle',
    'raw_query',
    'redirects_tests',
    # TODO: 'requests',
    'reserved_names',
    'resolve_url',
    # TODO: 'responses',
    'reverse_lookup',
    'save_delete_hooks',
    'schema',
    # TODO: 'select_for_update',
    'select_related',
    'select_related_onetoone',
    'select_related_regress',
    # TODO: 'serializers',
    # TODO: 'servers',
    'sessions_tests',
    'settings_tests',
    'shell',
    # TODO: 'shortcuts',
    # TODO: 'signals',
    'signed_cookies_tests',
    # TODO: 'signing',
    # TODO: 'sitemaps_tests',
    'sites_framework',
    # TODO: 'sites_tests',
    # TODO: 'staticfiles_tests',
    'str',
    'string_lookup',
    'swappable_models',
    # TODO: 'syndication_tests',
    # TODO: 'template_backends',
    'template_loader',
    # TODO: 'template_tests',
    # TODO: 'test_client',
    # TODO: 'test_client_regress',
    'test_exceptions',
    # TODO: 'test_runner',
    'test_runner_apps',
    # TODO: 'test_utils',
    # TODO: 'timezones',
    'transaction_hooks',
    # TODO: 'transactions',
    'unmanaged_models',
    # TODO: 'update',
    'update_only_fields',
    'urlpatterns',
    # TODO: 'urlpatterns_reverse',
    'user_commands',
    # TODO: 'utils_tests',
    # TODO: 'validation',
    'validators',
    'version',
    # TODO: 'view_tests',
    # TODO: 'wsgi',
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


def is_ignored(line: str, test_folder_name: str) -> bool:
    for pattern in IGNORED_ERRORS['__common__'] + IGNORED_ERRORS.get(test_folder_name, []):
        if isinstance(pattern, Pattern):
            if pattern.search(line):
                return True
        else:
            if pattern in line:
                return True
    return False


def replace_with_clickable_location(error: str, abs_test_folder: Path) -> str:
    raw_path, _, error_line = error.partition(': ')
    fname, line_number = raw_path.split(':')
    path = abs_test_folder.joinpath(fname).relative_to(PROJECT_DIRECTORY)
    clickable_location = f'./{path}:{line_number}'
    return error.replace(raw_path, clickable_location)


def check_with_mypy(abs_path: Path, config_file_path: Path) -> int:
    error_happened = False
    with cd(abs_path):
        sources, options = process_options(['--config-file', str(config_file_path), str(abs_path)])
        res = build.build(sources, options)
        for error_line in res.errors:
            if not is_ignored(error_line, abs_path.name):
                error_happened = True
                print(replace_with_clickable_location(error_line, abs_test_folder=abs_path))
    return int(error_happened)


if __name__ == '__main__':
    mypy_config_file = (PROJECT_DIRECTORY / 'scripts' / 'mypy.ini').absolute()
    repo_directory = PROJECT_DIRECTORY / 'django-sources'
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
        abs_path = (PROJECT_DIRECTORY / tests_root / dirname).absolute()
        print(f'Checking {abs_path}')

        rc = check_with_mypy(abs_path, mypy_config_file)
        if rc != 0:
            global_rc = 1

    sys.exit(rc)
