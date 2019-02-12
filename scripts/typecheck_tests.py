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
MOCK_OBJECTS = ['MockRequest', 'MockCompiler', 'modelz', 'call_count', 'call_args_list', 'call_args']
IGNORED_ERRORS = {
    '__common__': [
        *MOCK_OBJECTS,
        'LazySettings',
        'NullTranslations',
        'Need type annotation for',
        'Invalid value for a to= parameter',
        'already defined (possibly by an import)',
        'Cannot assign to a type',
        re.compile(r'Cannot assign to class variable "[a-z_]+" via instance'),
        # forms <-> models plugin support
        '"Model" has no attribute',
        re.compile(r'Cannot determine type of \'(objects|stuff)\''),
        # settings
        re.compile(r'Module has no attribute "[A-Z_]+"'),
        # attributes assigned to test functions
        re.compile(r'"Callable\[(\[(Any(, )?)*((, )?VarArg\(Any\))?((, )?KwArg\(Any\))?\]|\.\.\.), Any\]" has no attribute'),
        # assign empty tuple
        re.compile(r'Incompatible types in assignment \(expression has type "Tuple\[\]", '
                   r'variable has type "Tuple\[[A-Za-z, ]+\]"'),
        # assign method to a method
        'Cannot assign to a method',
        'Cannot infer type of lambda',
        re.compile(r'Incompatible types in assignment \(expression has type "Callable\[\[(Any(, )?)+\], Any\]", '
                   r'variable has type "Callable\['),
        # cookies private attribute
        'full_clean" of "Model" does not return a value',
        # private members
        re.compile(r'has no attribute "|\'_[a-z][a-z_]+"|\''),
        'Invalid base class',
        'ValuesIterable'
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
    'admin_utils': [
        re.compile(r'Argument [0-9] to "lookup_field" has incompatible type'),
        'MockModelAdmin',
        'Incompatible types in assignment (expression has type "str", variable has type "Callable[..., Any]")',
        'Dict entry 0 has incompatible type "str": "Tuple[str, str, List[str]]"; expected "str": '
        + '"Tuple[str, str, Tuple[str, str]]"',
        'Incompatible types in assignment (expression has type "bytes", variable has type "str")'
    ],
    'admin_views': [
        'Argument 1 to "FileWrapper" has incompatible type "StringIO"; expected "IO[bytes]"',
        'Incompatible types in assignment',
        '"object" not callable',
        'Incompatible type for "pk" of "Collector" (got "int", expected "str")',
        re.compile('Unexpected attribute "[a-z]+" for model "Model"'),
        'Unexpected attribute "two_id" for model "CyclicOne"'
    ],
    'aggregation': [
        'Incompatible types in assignment (expression has type "QuerySet[Any]", variable has type "List[Any]")',
        '"as_sql" undefined in superclass',
        'Incompatible types in assignment (expression has type "FlatValuesListIterable", '
        + 'variable has type "ValuesListIterable")'
    ],
    'aggregation_regress': [
        'Incompatible types in assignment (expression has type "List[str]", variable has type "QuerySet[Author]")',
        'Incompatible types in assignment (expression has type "FlatValuesListIterable", variable has type "QuerySet[Any]")',
        'Too few arguments for "count" of "Sequence"'
    ],
    'apps': [
        'Incompatible types in assignment (expression has type "str", target has type "type")',
        '"Callable[[bool, bool], List[Type[Model]]]" has no attribute "cache_clear"'
    ],
    'auth_tests': [
        '"PasswordValidator" has no attribute "min_length"',
        '"validate_password" does not return a value',
        '"password_changed" does not return a value',
        re.compile(r'"validate" of "([A-Za-z]+)" does not return a value'),
        'Module has no attribute "SessionStore"'
    ],
    'basic': [
        'Unexpected keyword argument "unknown_kwarg" for "refresh_from_db" of "Model"',
        '"refresh_from_db" of "Model" defined here',
        'Unexpected attribute "foo" for model "Article"'
    ],
    'builtin_server': [
        'has no attribute "getvalue"'
    ],
    'custom_lookups': [
        'in base class "SQLFuncMixin"'
    ],
    'custom_managers': [
        '_filter_CustomQuerySet',
        '_filter_CustomManager',
        re.compile(r'Cannot determine type of \'(abstract_persons|cars|plain_manager)\''),
        # TODO: remove after 'objects' and '_default_manager' are handled in the plugin
        'Incompatible types in assignment (expression has type "CharField", '
        + 'base class "Model" defined the type as "Manager[Model]")',
        # TODO: remove after from_queryset() handled in the plugin
        'Invalid base class'
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
    'dispatch': [
        'Argument 1 to "connect" of "Signal" has incompatible type "object"; expected "Callable[..., Any]"'
    ],
    'db_typecasts': [
        '"object" has no attribute "__iter__"; maybe "__str__" or "__dir__"? (not iterable)'
    ],
    'expressions': [
        'Argument 1 to "Subquery" has incompatible type "Sequence[Dict[str, Any]]"; expected "QuerySet[Any]"'
    ],
    'from_db_value': [
        'has no attribute "vendor"'
    ],
    'field_deconstruction': [
        'Incompatible types in assignment (expression has type "ForeignKey[Any]", variable has type "CharField")'
    ],
    'get_object_or_404': [
        'Argument 1 to "get_object_or_404" has incompatible type "str"; '
        + 'expected "Union[Type[Model], Manager[Any], QuerySet[Any]]"',
        'Argument 1 to "get_object_or_404" has incompatible type "Type[CustomClass]"; '
        + 'expected "Union[Type[Model], Manager[Any], QuerySet[Any]]"',
        'Argument 1 to "get_list_or_404" has incompatible type "List[Type[Article]]"; '
        + 'expected "Union[Type[Model], Manager[Any], QuerySet[Any]]"'
    ],
    'get_or_create': [
        'Argument 1 to "update_or_create" of "QuerySet" has incompatible type "**Dict[str, object]"; expected "MutableMapping[str, Any]"'
    ],
    'httpwrappers': [
        'Argument 2 to "appendlist" of "QueryDict" has incompatible type "List[str]"; expected "str"'
    ],
    'invalid_models_tests': [
        'Argument "max_length" to "CharField" has incompatible type "str"; expected "Optional[int]"',
        'Argument "choices" to "CharField" has incompatible type "str"'
    ],
    'model_inheritance_regress': [
        'Incompatible types in assignment (expression has type "List[Supplier]", variable has type "QuerySet[Supplier]")'
    ],
    'model_meta': [
        '"object" has no attribute "items"',
        '"Field" has no attribute "many_to_many"'
    ],
    'model_fields': [
        'Incompatible types in assignment (expression has type "Type[Person]", variable has type',
        'Unexpected keyword argument "name" for "Person"',
        'Cannot assign multiple types to name "PersonTwoImages" without an explicit "Type[...]" annotation',
    ],
    'model_regress': [
        'Too many arguments for "Worker"',
        re.compile(r'Incompatible type for "[a-z]+" of "Worker" \(got "int", expected')
    ],
    'modeladmin': [
        'BandAdmin',
        'base class "ModelAdmin" defined the type a',
        'base class "InlineModelAdmin" defined the type a',
        'List item 0 has incompatible type "Type[ValidationTestInline]"; expected "Type[InlineModelAdmin]"'
    ],
    'migrate_signals': [
        'Value of type "None" is not indexable',
    ],
    'migrations': [
        'FakeMigration',
        'Incompatible types in assignment (expression has type "TextField", base class "Model" '
        + 'defined the type as "Manager[Model]")',
        'Incompatible types in assignment (expression has type "DeleteModel", variable has type "RemoveField")',
        'Argument "bases" to "CreateModel" has incompatible type "Tuple[Type[Mixin], Type[Mixin]]"; '
        + 'expected "Optional[Sequence[Union[Type[Model], str]]]"',
        'Argument 1 to "RunPython" has incompatible type "str"; expected "Callable[..., Any]"',
        'FakeLoader',
        'Argument 1 to "append" of "list" has incompatible type "AddIndex"; expected "CreateModel"'
    ],
    'queryset_pickle': [
        '"None" has no attribute "somefield"'
    ],
    'postgres_tests': [
        'Cannot assign multiple types to name',
        'Incompatible types in assignment (expression has type "Type[Field]',
        'DummyArrayField',
        'DummyJSONField',
        'Argument "encoder" to "JSONField" has incompatible type "DjangoJSONEncoder"; expected "Optional[Type[JSONEncoder]]"',
        'for model "CITestModel"'
    ],
    'properties': [
        re.compile('Unexpected attribute "(full_name|full_name_2)" for model "Person"')
    ],
    'requests': [
        'Incompatible types in assignment (expression has type "Dict[str, str]", variable has type "QueryDict")'
    ],
    'responses': [
        'Argument 1 to "TextIOWrapper" has incompatible type "HttpResponse"; expected "IO[bytes]"'
    ],
    'prefetch_related': [
        'Incompatible types in assignment (expression has type "List[Room]", variable has type "QuerySet[Room]")',
        '"None" has no attribute "__iter__"',
        'has no attribute "read_by"'
    ],
    'signals': [
        'Argument 1 to "append" of "list" has incompatible type "Tuple[Any, Any, Any, Any]"; expected "Tuple[Any, Any, Any]"'
    ],
    'syndication_tests': [
        'List or tuple expected as variable arguments'
    ],
    'staticfiles_tests': [
        'Value of type "stat_result" is not indexable',
        '"setUp" undefined in superclass',
        'Argument 1 to "write" of "IO" has incompatible type "bytes"; expected "str"',
        'Value of type "object" is not indexable'
    ],
    'transactions': [
        'Incompatible types in assignment (expression has type "Thread", variable has type "Callable[[], Any]")'
    ],
    'test_client': [
        'Incompatible types in assignment (expression has type "StreamingHttpResponse", variable has type "HttpResponse")',
        'Incompatible types in assignment (expression has type "HttpResponse", variable has type "StreamingHttpResponse")'
    ],
    'test_client_regress': [
        'Incompatible types in assignment (expression has type "Dict[<nothing>, <nothing>]", variable has type "SessionBase")'
    ],
    'timezones': [
        'Too few arguments for "render" of "Template"'
    ],
    'test_runner': [
        'Value of type "TestSuite" is not indexable',
        '"TestSuite" has no attribute "_tests"',
        'Argument "result" to "run" of "TestCase" has incompatible type "RemoteTestResult"; expected "Optional[TestResult]"',
        'Item "TestSuite" of "Union[TestCase, TestSuite]" has no attribute "id"',
        'MockTestRunner',
        'Incompatible types in assignment (expression has type "Tuple[Union[TestCase, TestSuite], ...]", '
        + 'variable has type "TestSuite")'
    ],
    'template_tests': [
        'Xtemplate',
        re.compile(r'Argument 1 to "[a-zA-Z_]+" has incompatible type "int"; expected "str"'),
        'TestObject',
        'variable has type "Callable[[Any], Any]',
        'template_debug',
        '"yield from" can\'t be applied to',
        re.compile(r'List item [0-9] has incompatible type "URLResolver"; expected "URLPattern"'),
        '"WSGIRequest" has no attribute "current_app"'
    ],
    'template_backends': [
        'Incompatible import of "Jinja2" (imported name has type "Type[Jinja2]", local name has type "object")',
        'TemplateStringsTests'
    ],
    'urlpatterns': [
        '"object" has no attribute "__iter__"; maybe "__str__" or "__dir__"? (not iterable)',
        '"object" not callable'
    ],
    'user_commands': [
        'Incompatible types in assignment (expression has type "Callable[[Any, KwArg(Any)], Any]", variable has type'
    ],
    'utils_tests': [
        re.compile(r'Argument ([1-9]) to "__get__" of "classproperty" has incompatible type')
    ],
    'urlpatterns_reverse': [
        'to "reverse" has incompatible type "object"',
        'Module has no attribute "_translations"',
        "'django.urls.resolvers.ResolverMatch' object is not iterable"
    ],
    'sessions_tests': [
        'base class "SessionTestsMixin" defined the type as "None")'
    ],
    'select_related_onetoone': [
        '"None" has no attribute'
    ],
    'view_tests': [
        '"Handler" has no attribute "include_html"',
        '"EmailMessage" has no attribute "alternatives"'
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
    'admin_utils',
    'admin_views',
    'admin_widgets',
    'aggregation',
    'aggregation_regress',
    'annotations',
    'app_loading',
    'apps',
    # TODO: 'auth_tests',
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
    'custom_lookups',
    'custom_managers',
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
    'dispatch',
    'distinct_on_fields',
    'empty',
    'expressions',
    'expressions_case',
    # TODO: 'expressions_window',
    # TODO: 'extra_regress',
    'field_deconstruction',
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
    'get_or_create',
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

    # not practical
    # 'invalid_models_tests',

    'known_related_objects',
    # TODO: 'logging_tests',
    'lookup',
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
    'migrations',
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
    'modeladmin',
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
    'postgres_tests',
    'project_template',
    'properties',
    'proxy_model_inheritance',
    # TODO: 'proxy_models',
    # TODO: 'queries',
    'queryset_pickle',
    'raw_query',
    'redirects_tests',
    'requests',
    'reserved_names',
    'resolve_url',
    'responses',
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
    'shortcuts',
    'signals',
    'signed_cookies_tests',
    'signing',
    # TODO: 'sitemaps_tests',
    'sites_framework',
    'sites_tests',
    # TODO: 'staticfiles_tests',
    'str',
    'string_lookup',
    'swappable_models',
    'syndication_tests',
    'template_backends',
    'template_loader',
    'template_tests',
    'test_client',
    'test_client_regress',
    'test_exceptions',
    'test_runner',
    'test_runner_apps',
    'test_utils',
    'timezones',
    'transaction_hooks',
    'transactions',
    'unmanaged_models',
    'update',
    'update_only_fields',
    'urlpatterns',
    # not annotatable without annotation in test
    # TODO: 'urlpatterns_reverse',
    'user_commands',
    # TODO: 'utils_tests',
    # not annotatable without annotation in test
    # TODO: 'validation',
    'validators',
    'version',
    'view_tests',
    'wsgi',
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
    fname, _, line_number = raw_path.partition(':')

    try:
        path = abs_test_folder.joinpath(fname).relative_to(PROJECT_DIRECTORY)
    except ValueError:
        # fail on travis, just show an error
        return error

    clickable_location = f'./{path}:{line_number or 1}'
    return error.replace(raw_path, clickable_location)


def check_with_mypy(abs_path: Path, config_file_path: Path) -> int:
    error_happened = False
    with cd(abs_path):
        sources, options = process_options(['--cache-dir', str(config_file_path.parent / '.mypy_cache'),
                                            '--config-file', str(config_file_path),
                                            str(abs_path)])
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

    sys.exit(global_rc)
