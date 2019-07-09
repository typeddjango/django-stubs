import itertools
import os
import re
import shutil
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Pattern

from git import Repo
from mypy import build
from mypy.main import process_options

PROJECT_DIRECTORY = Path(__file__).parent.parent

# Django branch to typecheck against
DJANGO_BRANCH = 'stable/2.2.x'

# Specific commit in the Django repository to check against
DJANGO_COMMIT_SHA = '395cf7c37514b642c4bcf30e01fc1a2c4f82b2fe'

# Some errors occur for the test suite itself, and cannot be addressed via django-stubs. They should be ignored
# using this constant.
MOCK_OBJECTS = ['MockRequest', 'MockCompiler', 'modelz', 'call_count', 'call_args_list', 'call_args', 'MockUser']
IGNORED_ERRORS = {
    '__common__': [
        *MOCK_OBJECTS,
        'LazySettings',
        'NullTranslations',
        'Need type annotation for',
        'Invalid value for a to= parameter',
        'already defined (possibly by an import)',
        'already defined on line',
        'gets multiple values for keyword argument',
        'Cannot assign to a type',
        re.compile(r'Cannot assign to class variable "[a-z_]+" via instance'),
        # forms <-> models plugin support
        # '"Model" has no attribute',
        re.compile(r'Cannot determine type of \'(objects|stuff)\''),
        # settings
        re.compile(r'Module has no attribute "[A-Z_]+"'),
        # attributes assigned to test functions
        re.compile(
            r'"Callable\[(\[(Any(, )?)*((, )?VarArg\(Any\))?((, )?KwArg\(Any\))?\]|\.\.\.), Any\]" has no attribute'),
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
        re.compile(r'has no attribute ("|\')_[a-zA-Z_]+("|\')'),
        'Invalid base class',
        'ValuesIterable',
        'Value of type "Optional[Dict[str, Any]]" is not indexable',
        'Argument 1 to "len" has incompatible type "Optional[List[_Record]]"; expected "Sized"',
        'Argument 1 to "loads" has incompatible type "Union[bytes, str, None]"; '
        + 'expected "Union[str, bytes, bytearray]"',
        'Incompatible types in assignment (expression has type "None", variable has type Module)',
        'note:',
        '\'Settings\' object has no attribute',
        re.compile(r'"Type\[Model\]" has no attribute "[a-zA-Z_]+"'),
        re.compile(r'Item "None" of "[a-zA-Z_ ,\[\]]+" has no attribute'),
        'Xtemplate',
        re.compile(r'has no attribute "get_[a-z_]+_display"'),
        re.compile(r'has no attribute "get_next_by_[a-z_]+"'),
        re.compile(r'has no attribute "get_previous_by_[a-z_]+"'),
        re.compile(r'has no attribute "set_[a-z_]+_order"'),
        'psycopg2',
        'PIL',
        'has no attribute "getvalue"',
        'MySQLdb',
        'sqlparse',
        'selenium',
        'oracle',
        'mysql',
        'sqlite3',
        'LogEntry',
        '"HttpResponse" has no attribute',
        '"HttpResponseBase" has no attribute',
        '"object" has no attribute',
        '"HttpRequest" has no attribute',
        'xml.dom',
        'numpy',
        'tblib',
        # TODO: values().annotate()
        'TypedDict',
        'namedtuple',
        'has no attribute "deconstruct"',
        '**Dict',
        'undefined in superclass'
    ],
    'admin_scripts': [
        'Incompatible types in assignment (expression has type "Callable['
    ],
    'admin_utils': [
        re.compile(r'Argument [0-9] to "lookup_field" has incompatible type'),
        'MockModelAdmin',
        'Incompatible types in assignment (expression has type "str", variable has type "Callable[..., Any]")',
        '"Article" has no attribute "non_field"'
    ],
    'admin_views': [
        'Argument 1 to "FileWrapper" has incompatible type "StringIO"; expected "IO[bytes]"',
        'Incompatible types in assignment',
        '"object" not callable',
        '"Type[SubscriberAdmin]" has no attribute "overridden"'
    ],
    'admin_ordering': [
        '"Band" has no attribute "field"'
    ],
    'aggregation': [
        'Incompatible type for "contact" of "Book" (got "Optional[Author]", expected "Union[Author, Combinable]")',
        'Incompatible type for "publisher" of "Book" (got "Optional[Publisher]", '
        + 'expected "Union[Publisher, Combinable]")',
        'has no attribute'
    ],
    'aggregation_regress': [
        'has no attribute'
    ],
    'annotations': [
        'Incompatible type for "store" of "Employee" (got "Optional[Store]", expected "Union[Store, Combinable]")',
        '"Book" has no attribute',
        '"Employee" has no attribute',
        'Item "Book" of',
        'Item "Ticket" of'
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
        'Unexpected attribute "foo" for model "Article"',
        'has no attribute'
    ],
    'backends': [
        '"DatabaseError" has no attribute "pgcode"'
    ],
    'check_framework': [
        'base class "Model" defined the type as "Callable',
        'Cannot determine type of \'check\''
    ],
    'constraints': [
        'Argument "condition" to "UniqueConstraint" has incompatible type "str"; expected "Optional[Q]"'
    ],
    'contenttypes_tests': [
        'Item "Model" of "Union[GenericForeignKey, Model, None]" has no attribute'
    ],
    'custom_lookups': [
        'in base class "SQLFuncMixin"'
    ],
    'custom_pk': [
        '"Employee" has no attribute "id"'
    ],
    'custom_managers': [
        '"Type[Book]" has no attribute "objects"'
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
        'Argument 1 to "connect" of "Signal" has incompatible type "object"; expected "Callable[..., Any]"',
        'Item "str" of "Union[ValueError, str]" has no attribute "args"'
    ],
    'deprecation': [
        '"Manager" has no attribute "old"',
        '"Manager" has no attribute "new"'
    ],
    'db_functions': [
        'for **',
        'expected "float"',
        'Incompatible types in assignment (expression has type "Optional[FloatModel]", variable has type "FloatModel")',
        re.compile(r'Item .* has no attribute'),
        'Module has no attribute',
        'Module \'datetime\' has no attribute',
        '"DTModel" has no attribute',
        '"Author" has no attribute',
        '"FloatModel" has no attribute',
        '"Article" has no attribute'
    ],
    'decorators': [
        'DummyRequest',
        'DummyUser',
        '"Type[object]" has no attribute "method"'
    ],
    'defer_regress': [
        '"Base" has no attribute "derived"'
    ],
    'delete': [
        '"RChild" has no attribute',
        '"Child" has no attribute "parent_ptr"'
    ],
    'expressions': [
        'Item "Experiment" of',
        'Item "Time" of',
        '"Experiment" has no attribute',
        '"Time" has no attribute',
    ],
    'expressions_case': [
        '"CaseTestModel" has no attribute "selected"'
    ],
    'expressions_window': [
        'has incompatible type "str"'
    ],
    'file_uploads': [
        '"Iterable[Any]" has no attribute',
        '"IO[Any]" has no attribute'
    ],
    'file_storage': [
        'Incompatible types in assignment (expression has type "Callable[[], Any]"'
    ],
    'files': [
        '"file_move_safe" does not return a value',
        'Incompatible types in assignment (expression has type "IOBase", variable has type "File")',
        'Module has no attribute "open"'
    ],
    'fixtures': [
        'Incompatible types in assignment (expression has type "int", target has type "Iterable[str]")'
    ],
    'flatpages_tests': [
        '"Site" has no attribute "add"',
    ],
    'forms_tests': [
        'List item 0 has incompatible type "Jinja2"; expected "DjangoTemplates"',
        'Not enough arguments for format string',
        'Argument after ** must be a mapping, not "object"',
        'expression has type "None", base class "TestFormParent"',
        'variable has type "SongForm"',
        '"full_clean" of "BaseForm" does not return a value',
        'No overload variant of "zip" matches argument types "Tuple[str, str, str]", "object"',
        'Incompatible types in assignment (expression has type "GetDateShowHiddenInitial", '
        + 'variable has type "GetDate")',
        re.compile(r'Incompatible types in assignment \(expression has type "[a-zA-Z]+Field", '
                   r'base class "BaseForm" defined the type as "Dict\[str, Any\]"\)'),
        'List or tuple expected as variable arguments',
        'Argument 1 to "__init__" of "MultiWidget" has incompatible type "List[object]"; '
        + 'expected "Sequence[Union[Widget, Type[Widget]]]"',
        'Argument 1 to "issubclass" has incompatible type "ModelFormMetaclass"; expected "type"',
        'Incompatible types in assignment (expression has type "List[str]", target has type "str")',
        'Incompatible types in assignment (expression has type "TestForm", variable has type "Person")',
        'Incompatible types in assignment (expression has type "Type[Textarea]", '
        + 'base class "Field" defined the type as "Widget")',
        'Incompatible types in assignment (expression has type "SimpleUploadedFile", variable has type "BinaryIO")',
        'has no attribute',
        'Name \'forms.Field\' is not defined'
    ],
    'foreign_object': [
        '"Person" has no attribute',
        '"SlugPage" has no attribute'
    ],
    'from_db_value': [
        '"Cash" has no attribute'
    ],
    'get_object_or_404': [
        'Argument 1 to "get_object_or_404" has incompatible type "str"; '
        + 'expected "Union[Type[<nothing>], QuerySet[<nothing>, <nothing>]]"',
        'Argument 1 to "get_list_or_404" has incompatible type "List[Type[Article]]"; '
        + 'expected "Union[Type[<nothing>], QuerySet[<nothing>, <nothing>]]"',
        'CustomClass'
    ],
    'generic_relations': [
        'has no attribute "id"',
        'has no attribute "pk"'
    ],
    'generic_relations_regress': [
        '"HasLinkThing" has no attribute',
        '"Link" has no attribute'
    ],
    'humanize_tests': [
        'Argument 1 to "append" of "list" has incompatible type "None"; expected "str"'
    ],
    'inline_formsets': [
        'has no attribute "form"'
    ],
    'logging_tests': [
        '"Handler" has no attribute "stream"'
    ],
    'lookup': [
        'Unexpected keyword argument "headline__startswith" for "in_bulk" of "QuerySet"',
        '\'flat\' is not valid when values_list is called with more than one field.'
    ],
    'm2o_recursive': [
        'Incompatible type for "id" of "Category" (got "None", expected "int")'
    ],
    'many_to_one': [
        'Incompatible type for "parent" of "Child" (got "None", expected "Union[Parent, Combinable]")',
        'Incompatible type for "parent" of "Child" (got "Child", expected "Union[Parent, Combinable]")'
    ],
    'managers_regress': [
        '"Type[AbstractBase3]" has no attribute "objects"'
    ],
    'middleware_exceptions': [
        'Argument 1 to "append" of "list" has incompatible type "Tuple[Any, Any]"; expected "str"'
    ],
    'model_fields': [
        'Incompatible types in assignment (expression has type "Type[Person]", variable has type',
        'Unexpected keyword argument "name" for "Person"',
        'Cannot assign multiple types to name "PersonTwoImages" without an explicit "Type[...]" annotation',
        re.compile(
            r'Incompatible types in assignment \(expression has type "Type\[.+?\]", base class "IntegerFieldTests"'
            r' defined the type as "Type\[IntegerModel\]"\)'),
        re.compile(r'Incompatible types in assignment \(expression has type "Type\[.+?\]", base class'
                   r' "ImageFieldTestMixin" defined the type as "Type\[PersonWithHeightAndWidth\]"\)'),
        'Incompatible import of "Person"',
        'Incompatible types in assignment (expression has type "FloatModel", variable has type '
        '"Union[float, int, str, Combinable]")',
        '"UUIDGrandchild" has no attribute "uuidchild_ptr_id"',
        '"Person" has no attribute',
        '"Foo" has no attribute',
    ],
    'model_formsets': [
        'has no attribute'
    ],
    'model_indexes': [
        'Argument "condition" to "Index" has incompatible type "str"; expected "Optional[Q]"'
    ],
    'model_inheritance_regress': [
        '"Restaurant" has no attribute',
        '"ArticleWithAuthor" has no attribute',
        '"Person" has no attribute',
        '"MessyBachelorParty" has no attribute',
        '"Place" has no attribute',
        '"ItalianRestaurant" has no attribute'
    ],
    'model_meta': [
        '"Field[Any, Any]" has no attribute "many_to_many"'
    ],
    'model_regress': [
        re.compile(r'Incompatible type for "[a-z]+" of "Worker" \(got "int", expected'),
        '"PickledModel" has no attribute',
        '"Department" has no attribute'
    ],
    'modeladmin': [
        'BandAdmin',
        'base class "ModelAdmin" defined the type a',
        'base class "InlineModelAdmin" defined the type a',
        'List item 0 has incompatible type',
        'Incompatible types in assignment (expression has type "None", base class "AdminBase" '
        + 'defined the type as "List[str]")'
    ],
    'migrate_signals': [
        'Value of type "None" is not indexable',
        'Argument 1 to "set" has incompatible type "None"; expected "Iterable[<nothing>]"'
    ],
    'migrations': [
        'FakeMigration',
        'FakeLoader',
        'Dict entry 0 has incompatible type "Any": "Set[Tuple[Any, ...]]"; expected "Any": "str"',
        'Argument 1 to "RunPython" has incompatible type "str"; expected "Callable[..., Any]"',
        'Argument 1 to "append" of "list" has incompatible type "AddIndex"; expected "CreateModel"',
        'Argument 2 to "register_serializer" of "MigrationWriter" has incompatible type '
        + '"Type[TestModel1]"; expected "Type[BaseSerializer]"',
        'Argument 1 to "append" of "list" has incompatible type "AddConstraint"; expected "CreateModel"'
    ],
    'multiple_database': [
        'Too many arguments for "create" of "QuerySet"',
        '"User" has no attribute "userprofile"',
        'Item "GenericForeignKey" of',
        'Item "Model" of'
    ],
    'known_related_objects': [
        '"Pool" has no attribute'
    ],
    'one_to_one': [
        '"Place" has no attribute',
        '"Type[Place]" has no attribute',
        '"ManualPrimaryKey" has no attribute'
    ],
    'postgres_tests': [
        'DummyArrayField',
        'DummyJSONField',
        'Cannot assign multiple types to name',
        'Incompatible types in assignment (expression has type "Type[Field[Any, Any]]',
        'Argument "encoder" to "JSONField" has incompatible type "DjangoJSONEncoder"; '
        + 'expected "Optional[Type[JSONEncoder]]"',
        'Incompatible type for "field" of "IntegerArrayModel" (got "None", '
        + 'expected "Union[Sequence[int], Combinable]")',
        re.compile(r'Incompatible types in assignment \(expression has type "Type\[.+?\]", '
                   r'base class "(UnaccentTest|TrigramTest)" defined the type as "Type\[CharFieldModel\]"\)'),
        '"Type[PostgreSQLModel]" has no attribute "objects"',
        '("None" and "SearchQuery")',
        # TODO:
        'django.contrib.postgres.forms',
        'django.contrib.postgres.aggregates',
    ],
    'properties': [
        re.compile('Unexpected attribute "(full_name|full_name_2)" for model "Person"')
    ],
    'prefetch_related': [
        'Incompatible types in assignment (expression has type "List[Room]", variable has type "QuerySet[Room, Room]")',
        '"Person" has no attribute',
        '"Author" has no attribute',
        '"Book" has no attribute',
        'Item "Room" of',
        '"AuthorWithAge" has no attribute',
        'has no attribute "read_by"'
    ],
    'proxy_model_inheritance': [
        'Incompatible import of "ProxyModel"'
    ],
    'queries': [
        'Incompatible types in assignment (expression has type "None", variable has type "str")',
        'Invalid index type "Optional[str]" for "Dict[str, int]"; expected type "str"',
        'No overload variant of "values_list" of "QuerySet" matches argument types "str", "bool", "bool"',
        'Unsupported operand types for & ("QuerySet[Author, Author]" and "QuerySet[Tag, Tag]")',
        'Unsupported operand types for | ("QuerySet[Author, Author]" and "QuerySet[Tag, Tag]")',
        'Incompatible types in assignment (expression has type "ObjectB", variable has type "ObjectA")',
        'Incompatible types in assignment (expression has type "ObjectC", variable has type "ObjectA")',
        'Incompatible type for "objectb" of "ObjectC" (got "ObjectA", expected'
        ' "Union[ObjectB, Combinable, None, None]")',
        '"Note" has no attribute',
        '"Ranking" has no attribute',
        '"BaseUser" has no attribute',
        '"Item" has no attribute',
        "'flat' and 'named' can't be used together.",
    ],
    'queryset_pickle': [
        'RelatedObjectDoesNotExist',
        '"Type[Event]" has no attribute "happening"'
    ],
    'requests': [
        'Incompatible types in assignment (expression has type "Dict[str, str]", variable has type "QueryDict")'
    ],
    'responses': [
        'Argument 1 to "TextIOWrapper" has incompatible type "HttpResponse"; expected "IO[bytes]"'
    ],
    'schema': [
        'Incompatible type for "info" of "Note" (got "None", expected "Union[str, Combinable]")',
        'Incompatible type for "detail_info" of "NoteRename" (got "None", expected "Union[str, Combinable]")',
        'Incompatible type for "year" of "UniqueTest" (got "None", expected "Union[float, int, str, Combinable]")'
    ],
    'settings_tests': [
        'Argument 1 to "Settings" has incompatible type "Optional[str]"; expected "str"'
    ],
    'signals': [
        'Argument 1 to "append" of "list" has incompatible type "Tuple[Any, Any, Optional[Any], Any]"; '
        + 'expected "Tuple[Any, Any, Any]"'
    ],
    'sites_tests': [
        'Item "RequestSite" of "Union[Site, RequestSite]" has no attribute "id"'
    ],
    'syndication_tests': [
        'List or tuple expected as variable arguments'
    ],
    'sessions_tests': [
        'base class "SessionTestsMixin" defined the type as "None")',
        'Incompatible types in assignment (expression has type "None", variable has type "int")',
        '"AbstractBaseSession" has no attribute'
    ],
    'select_related': [
        '"Species" has no attribute',
        'Item "object" of "Union[object, Any]" has no attribute "first"'
    ],
    'select_related_onetoone': [
        'Incompatible types in assignment (expression has type "Parent2", variable has type "Parent1")',
        'has no attribute'
    ],
    'servers': [
        re.compile('Argument [0-9] to "WSGIRequestHandler"'),
        '"HTTPResponse" has no attribute',
        '"type" has no attribute',
        '"WSGIRequest" has no attribute "makefile"'
    ],
    'template_tests': [
        re.compile(r'Argument 1 to "[a-zA-Z_]+" has incompatible type "int"; expected "str"'),
        'TestObject',
        'variable has type "Callable[[Any], Any]',
        'Value of type variable "AnyStr" of "urljoin" cannot be "Optional[str]"',
        'has no attribute "template_debug"',
        "Module 'django.template.base' has no attribute 'TemplateSyntaxError'"
    ],
    'template_backends': [
        'Incompatible import of "Jinja2" (imported name has type "Type[Jinja2]", local name has type "object")',
        'TemplateStringsTests',
        "Cannot find module named 'DoesNotExist'"
    ],
    'test_client': [
        'Incompatible types in assignment (expression has type "HttpResponse", '
        + 'variable has type "StreamingHttpResponse")'
    ],
    'test_client_regress': [
        'Incompatible types in assignment (expression has type "Dict[<nothing>, <nothing>]", '
        + 'variable has type "SessionBase")',
        'Unsupported left operand type for + ("None")',
    ],
    'timezones': [
        'Too few arguments for "render" of "Template"'
    ],
    'test_runner': [
        'Argument "result" to "run" of "TestCase" has incompatible type "RemoteTestResult"; '
        + 'expected "Optional[TestResult]"',
        'has no attribute "id"',
        'MockTestRunner'
    ],
    'transactions': [
        'Incompatible types in assignment (expression has type "Thread", variable has type "Callable[[], Any]")'
    ],
    'urlpatterns': [
        '"object" not callable'
    ],
    'user_commands': [
        'Incompatible types in assignment (expression has type "Callable[[Any, KwArg(Any)], Any]", variable has type',
        'Cannot find module named \'user_commands.management.commands\''
    ],
    'view_tests': [
        '"EmailMessage" has no attribute "alternatives"',
        '"Handler" has no attribute "include_html"',
        "Module 'django.views.debug' has no attribute 'Path'"
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
    'backends',
    'base',
    'bash_completion',
    'basic',
    'builtin_server',
    'bulk_create',
    # TODO: 'cache',
    'check_framework',
    'choices',
    'conditional_processing',
    'constraints',
    'contenttypes_tests',
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
    'decorators',
    'defer',
    'defer_regress',
    'delete',
    'delete_regress',
    'deprecation',
    'dispatch',
    'distinct_on_fields',
    'empty',
    'expressions',
    'expressions_case',
    'expressions_window',
    # TODO: 'extra_regress',
    'field_deconstruction',
    'field_defaults',
    'field_subclassing',
    'file_storage',
    'file_uploads',
    'files',
    'filtered_relation',
    'fixtures',
    'fixtures_model_package',
    'fixtures_regress',
    'flatpages_tests',
    'force_insert_update',
    'foreign_object',
    'forms_tests',
    'from_db_value',
    'generic_inline_admin',
    'generic_relations',
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
    'logging_tests',
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
    'middleware',
    'middleware_exceptions',
    'migrate_signals',
    'migration_test_data_persistence',
    'migrations',
    'migrations2',
    'model_fields',
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
    'multiple_database',
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
    'pagination',
    'postgres_tests',
    'prefetch_related',
    'project_template',
    'properties',
    'proxy_model_inheritance',
    # TODO: 'proxy_models',
    'queries',
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
    'servers',
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
    # 'urlpatterns_reverse',
    'user_commands',
    # TODO: 'utils_tests',
    'validation',
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
    for pattern in itertools.chain(IGNORED_ERRORS['__common__'],
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


def get_absolute_path_for_test(test_dirname: str):
    return (PROJECT_DIRECTORY / tests_root / test_dirname).absolute()


if __name__ == '__main__':
    mypy_config_file = (PROJECT_DIRECTORY / 'scripts' / 'mypy.ini').absolute()
    repo_directory = PROJECT_DIRECTORY / 'django-sources'
    mypy_cache_dir = Path(__file__).parent / '.mypy_cache'
    tests_root = repo_directory / 'tests'
    global_rc = 0

    # clone Django repository, if it does not exist
    if not repo_directory.exists():
        repo = Repo.clone_from('https://github.com/django/django.git', repo_directory)
    else:
        repo = Repo(repo_directory)
        repo.remotes['origin'].pull(DJANGO_BRANCH)

    repo.git.checkout(DJANGO_COMMIT_SHA)

    if len(sys.argv) > 1:
        tests_to_run = sys.argv[1:]
    else:
        tests_to_run = TESTS_DIRS

    try:
        for dirname in tests_to_run:
            abs_path = get_absolute_path_for_test(dirname)
            print(f'Checking {abs_path}')

            rc = check_with_mypy(abs_path, mypy_config_file)
            if rc != 0:
                global_rc = 1

        sys.exit(global_rc)

    except BaseException as exc:
        shutil.rmtree(mypy_cache_dir, ignore_errors=True)
        raise exc
