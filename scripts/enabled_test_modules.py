# Some errors occur for the test suite itself, and cannot be addressed via django-stubs. They should be ignored
# using this constant.
import re

IGNORED_MODULES = {'schema', 'gis_tests', 'admin_widgets', 'admin_filters', 'migrations',
                   'sitemaps_tests', 'staticfiles_tests', 'modeladmin', 'model_forms',
                   'generic_views', 'forms_tests', 'flatpages_tests', 'admin_utils',
                   'admin_ordering', 'admin_changelist', 'admin_views', 'mail', 'redirects_tests',
                   'invalid_models_tests', 'i18n', 'migrate_signals', 'model_formsets',
                   'template_tests', 'template_backends', 'test_runner', 'admin_scripts',
                   'sites_tests', 'inline_formsets', 'foreign_object', 'cache', 'test_client', 'test_client_regress'}

MOCK_OBJECTS = ['MockRequest', 'MockCompiler', 'modelz', 'call_count', 'call_args_list',
                'call_args', 'MockUser', 'Xtemplate', 'DummyRequest', 'DummyUser', 'MinimalUser']
EXTERNAL_MODULES = ['psycopg2', 'PIL', 'selenium', 'oracle', 'mysql', 'sqlite3', 'sqlparse', 'tblib', 'numpy',
                    'bcrypt', 'argon2', 'xml.dom']
IGNORED_ERRORS = {
    '__new_common__': [
        *MOCK_OBJECTS,
        *EXTERNAL_MODULES,
        'SupportsFloat',
        'Need type annotation for',
        'has no attribute "getvalue"',
        'Cannot assign to a method',
        'Cannot infer type of lambda',
        'already defined (possibly by an import)',
        'already defined on line',
        'Cannot assign to a type',
        '"HttpResponse" has no attribute',
        '"HttpResponseBase" has no attribute',
        # '"HttpRequest" has no attribute',
        '"object" has no attribute',
        'defined in the current module',
        re.compile(r'"Callable\[(\[(Any(, )?)*((, )?VarArg\(Any\))?((, )?KwArg\(Any\))?\]|\.\.\.), Any\]" '
                   r'has no attribute'),
        'has no attribute "deconstruct"',
        # private members
        re.compile(r'has no attribute ("|\')_[a-zA-Z_]+("|\')'),
        "'Settings' object has no attribute",
        '**Dict',
        re.compile(r"Expression of type '.*' is not supported"),
        'has incompatible type "object"',
        'undefined in superclass',
        'Argument after ** must be a mapping, not "object"',
        'note:',
        re.compile(r'Item "None" of "[a-zA-Z_ ,\[\]]+" has no attribute'),
        '"Optional[List[_Record]]"',
        '"Callable[..., None]" has no attribute',
        'does not return a value',
        'has no attribute "alternatives"',
        'gets multiple values for keyword argument',
        '"Handler" has no attribute',
        'Module has no attribute',
        "No installed app with label 'missing'",
        'namedtuple',
        'Lookups not supported yet',
        'Argument 1 to "loads" has incompatible type',
        # TODO: see test in managers/test_managers.yml
        "Cannot determine type of",
        'cache_clear',
        'cache_info',
        'Incompatible types in assignment (expression has type "None", variable has type Module)',
        "Module 'django.contrib.messages.storage.fallback' has no attribute 'CookieStorage'",
        # TODO: not supported yet
        'GenericRelation',
        'RelatedObjectDoesNotExist',
        # Rel's attributes are not accessible from `get_field()`
        re.compile(r'"Field\[Any, Any\]" has no attribute '
                   r'"(through|field_name|field|get_related_field|related_model|related_name'
                   r'|get_accessor_name|empty_strings_allowed|many_to_many)"'),
        # TODO: multitable inheritance
        'ptr',
        'Incompatible types in assignment (expression has type "Callable[',
        'SimpleLazyObject'
    ],
    'apps': [
        'Incompatible types in assignment (expression has type "str", target has type "type")',
    ],
    'auth_tests': [
        '"PasswordValidator" has no attribute "min_length"',
        'AbstractBaseUser',
        'Argument "password_validators" to "password_changed" has incompatible type "Tuple[Validator]"; '
        + 'expected "Optional[Sequence[PasswordValidator]]"',
        'Unsupported right operand type for in ("object")',
        'mock_getpass',
        'Unsupported left operand type for + ("Sequence[str]")',
        'AuthenticationFormWithInactiveUsersOkay',
        'Incompatible types in assignment (expression has type "Dict[str, Any]", variable has type "QueryDict")',
    ],
    'basic': [
        'Unexpected keyword argument "unknown_kwarg" for "refresh_from_db" of "Model"',
        'Unexpected attribute "foo" for model "Article"',
        'has no attribute "touched"'
    ],
    'backends': [
        '"DatabaseError" has no attribute "pgcode"'
    ],
    'check_framework': [
        'base class "Model" defined the type as "Callable',
    ],
    'constraints': [
        'Argument "condition" to "UniqueConstraint" has incompatible type "str"; expected "Optional[Q]"'
    ],
    'contenttypes_tests': [
        #     'Item "Model" of "Union[GenericForeignKey, Model, None]" has no attribute'
        'base class "BaseOrderWithRespectToTests" defined the type as "None"'
    ],
    'custom_lookups': [
        'in base class "SQLFuncMixin"'
    ],
    'custom_pk': [
        '"Employee" has no attribute "id"'
    ],
    'custom_managers': [
        'Unsupported dynamic base class',
        '"Book" has no attribute "favorite_avg"',
        'Incompatible types in assignment (expression has type "CharField'
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
        'Item "str" of "Union[ValueError, str]" has no attribute "args"'
    ],
    'deprecation': [
        '"Manager" has no attribute "old"',
        '"Manager" has no attribute "new"'
    ],
    'db_functions': [
        '"FloatModel" has no attribute',
    ],
    'decorators': [
        '"Type[object]" has no attribute "method"'
    ],
    'expressions_case': [
        'Item "Field[Any, Any]" of "Union[Field[Any, Any], ForeignObjectRel]" has no attribute "is_relation"'
    ],
    'expressions_window': [
        'has incompatible type "str"'
    ],
    'file_uploads': [
        '"Iterable[Any]" has no attribute',
        '"IO[Any]" has no attribute'
    ],
    'file_storage': [
        'Incompatible types in assignment (expression has type "Callable"'
    ],
    'files': [
        'Incompatible types in assignment (expression has type "IOBase", variable has type "File")',
    ],
    'fixtures': [
        'Incompatible types in assignment (expression has type "int", target has type "Iterable[str]")',
        'Incompatible types in assignment (expression has type "SpyManager[Spy]"'
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
    'generic_relations_regress': [
        '"Link" has no attribute'
    ],
    'httpwrappers': [
        'Argument 2 to "appendlist" of "QueryDict"',
        'Incompatible types in assignment (expression has type "int", target has type "Union[str, List[str]]")',
        'Argument 1 to "fromkeys" of "QueryDict" has incompatible type "int"'
    ],
    'humanize_tests': [
        'Argument 1 to "append" of "list" has incompatible type "None"; expected "str"'
    ],
    'lookup': [
        'Unexpected keyword argument "headline__startswith" for "in_bulk" of "QuerySet"',
        'is called with more than one field'
    ],
    'messages_tests': [
        'List item 0 has incompatible type "Dict[str, Message]"; expected "Message"'
    ],
    'middleware': [
        '"HttpRequest" has no attribute'
    ],
    'managers_regress': [
        '"Type[AbstractBase3]" has no attribute "objects"'
    ],
    'many_to_one': [
        'Incompatible type for "parent" of "Child" (got "None", expected "Union[Parent, Combinable]")',
        'Incompatible type for "parent" of "Child" (got "Child", expected "Union[Parent, Combinable]")'
    ],
    'middleware_exceptions': [
        'Argument 1 to "append" of "list" has incompatible type "Tuple[Any, Any]"; expected "str"'
    ],
    'model_fields': [
        'Item "Field[Any, Any]" of "Union[Field[Any, Any], ForeignObjectRel]" has no attribute',
        'has no attribute "field"',
        'Incompatible types in assignment (expression has type "Type[Person',
        'base class "IntegerFieldTests"',
        'ImageFieldTestMixin',
        'Incompatible types in assignment (expression has type "FloatModel", variable has type',
    ],
    'model_indexes': [
        'Argument "condition" to "Index" has incompatible type "str"; expected "Optional[Q]"'
    ],
    'model_inheritance': [
        'base class "AbstractBase" defined',
        'base class "AbstractModel" defined',
        'Definition of "name" in base class "ConcreteParent"',
        ' Definition of "name" in base class "AbstractParent"',
        'referent_references'
    ],
    'model_meta': [
        'List item 0 has incompatible type "str"; expected "Union[Field[Any, Any], ForeignObjectRel]"'
    ],
    'model_regress': [
        'Incompatible type for "department" of "Worker"',
        '"PickledModel" has no attribute',
        '"Department" has no attribute "evaluate"',
    ],
    'multiple_database': [
        'Unexpected attribute "extra_arg" for model "Book"'
    ],
    'order_with_respect_to': [
        'BaseOrderWithRespectToTests',
        '"Dimension" has no attribute "set_component_order"',
    ],
    'one_to_one': [
        'expression has type "None", variable has type "UndergroundBar"'
    ],
    'postgres_tests': [
        'DummyArrayField',
        'DummyJSONField',
        'Incompatible types in assignment (expression has type "Type[Field[Any, Any]]',
        'Argument "encoder" to "JSONField" has incompatible type "DjangoJSONEncoder";',
        re.compile(r'Incompatible types in assignment \(expression has type "Type\[.+?\]", '
                   r'base class "(UnaccentTest|TrigramTest)" defined the type as "Type\[CharFieldModel\]"\)'),
        '("None" and "SearchQuery")',
        # TODO:
        'django.contrib.postgres.forms',
        'django.contrib.postgres.aggregates',
    ],
    'properties': [
        re.compile('Unexpected attribute "(full_name|full_name_2)" for model "Person"')
    ],
    'prefetch_related': [
        '"Person" has no attribute "houses_lst"',
        '"Book" has no attribute "first_authors"',
        '"Book" has no attribute "the_authors"',
        'Incompatible types in assignment (expression has type "List[Room]", variable has type "QuerySet[Room, Room]")',
        '"Room" has no attribute "main_room_of_attr"',
        '"Room" has no attribute "house_attr"'
    ],
    'proxy_models': [
        'Incompatible types in assignment',
        'in base class "User"'
    ],
    'queries': [
        'Incompatible types in assignment (expression has type "None", variable has type "str")',
        'Invalid index type "Optional[str]" for "Dict[str, int]"; expected type "str"',
        'Unsupported operand types for & ("QuerySet[Author, Author]" and "QuerySet[Tag, Tag]")',
        'Unsupported operand types for | ("QuerySet[Author, Author]" and "QuerySet[Tag, Tag]")',
        'ObjectA',
        'ObjectB',
        'ObjectC',
        "'flat' and 'named' can't be used together",
    ],
    'requests': [
        'Incompatible types in assignment (expression has type "Dict[str, str]", variable has type "QueryDict")'
    ],
    'responses': [
        'Argument 1 to "TextIOWrapper" has incompatible type "HttpResponse"; expected "IO[bytes]"'
    ],
    'settings_tests': [
        'Argument 1 to "Settings" has incompatible type "Optional[str]"; expected "str"'
    ],
    'signals': [
        'Argument 1 to "append" of "list" has incompatible type "Tuple[Any, Any, Optional[Any], Any]";'
    ],
    'syndication_tests': [
        'List or tuple expected as variable arguments'
    ],
    'sessions_tests': [
        'base class "SessionTestsMixin" defined the type as "None")',
        'Incompatible types in assignment (expression has type "None", variable has type "int")',
        '"AbstractBaseSession" has no attribute'
    ],
    'select_related_onetoone': [
        'Incompatible types in assignment (expression has type "Parent2", variable has type "Parent1")',
        '"Parent1" has no attribute'
    ],
    'servers': [
        re.compile('Argument [0-9] to "WSGIRequestHandler"'),
        '"HTTPResponse" has no attribute',
        '"type" has no attribute',
        '"WSGIRequest" has no attribute "makefile"'
    ],
    'serializers': [
        '"SerializersTestBase" defined the type as "None"',
        '"Model" has no attribute "data"',
        '"Iterable[Any]" has no attribute "content"',
    ],
    'transactions': [
        'Incompatible types in assignment (expression has type "Thread", variable has type "Callable[[], Any]")'
    ],
    'urlpatterns': [
        '"object" not callable'
    ],
    'urlpatterns_reverse': [
        'List or tuple expected as variable arguments',
        'No overload variant of "zip" matches argument types "Any", "object"',
        'Argument 1 to "get_callable" has incompatible type "int"'
    ],
    'utils_tests': [
        'Too few arguments for "__init__"',
        'Argument 1 to "activate" has incompatible type "None"; expected "Union[tzinfo, str]"',
        'Incompatible types in assignment (expression has type "None", base class "object" defined the type as',
        'Class',
        'has no attribute "cp"',
        'Argument "name" to "cached_property" has incompatible type "int"; expected "Optional[str]"',
        'has no attribute "sort"',
        'Unsupported target for indexed assignment',
        'defined the type as "None"',
        'Argument 1 to "Path" has incompatible type "Optional[str]"'
    ],
    'view_tests': [
        "Module 'django.views.debug' has no attribute 'Path'"
    ]
}
