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
    'Definition of "as_sql" in base class',
    'expression has type "property"',
    '"object" has no attribute "__iter__"',
    'Too few arguments for "dates" of "QuerySet"',
    'has no attribute "vendor"',
    'Argument 1 to "get_list_or_404" has incompatible type "List',
    'error: "AdminRadioSelect" has no attribute "can_add_related"',
    'MockCompiler',
    'SessionTestsMixin',
    'Argument 1 to "Paginator" has incompatible type "ObjectList"',
    '"Type[Morsel[Any]]" has no attribute "_reserved"',
    'Argument 1 to "append" of "list"',
    'Argument 1 to "bytes"',
    '"full_clean" of "Model" does not return a value',
    '"object" not callable',
    'Item "GenericForeignKey" of "Union[GenericForeignKey, Model, None]" has no attribute "read_by"',
    'Item "Model" of "Union[GenericForeignKey, Model, None]" has no attribute "read_by"',
    re.compile('Cannot determine type of \'(objects|stuff|specimens|normal_manager)\''),
    re.compile(r'"Callable\[\[(Any(, )?)+\], Any\]" has no attribute'),
    re.compile(r'"HttpResponseBase" has no attribute "[A-Za-z_]+"'),
    re.compile(r'Incompatible types in assignment \(expression has type "Tuple\[\]", '
               r'variable has type "Tuple\[[A-Za-z, ]+\]"'),
    re.compile(r'"validate" of "[A-Za-z]+" does not return a value'),
    re.compile(r'Module has no attribute "[A-Za-z_]+"'),
    re.compile(r'"[A-Za-z\[\]]+" has no attribute "getvalue"'),
    # TODO: remove when reassignment will be possible (in 0.670? )
    re.compile(r'Incompatible types in assignment \(expression has type "(QuerySet|List)\[[A-Za-z, ]+\]", '
               r'variable has type "(QuerySet|List)\[[A-Za-z, ]+\]"\)'),
    re.compile(r'"(MockRequest|DummyRequest|DummyUser)" has no attribute "[a-zA-Z_]+"'),
    # TODO: remove when form <-> model plugin support is added
    re.compile(r'"Model" has no attribute "[A-Za-z_]+"'),
    re.compile(r'Argument 1 to "get_object_or_404" has incompatible type "(str|Type\[CustomClass\])"'),
    re.compile(r'"None" has no attribute "[a-zA-Z_0-9]+"'),
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
    # SKIPPED (all errors are false positives) 'migrate_signals',
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
    # SKIPPED (all errors are false positives) 'model_meta',
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
