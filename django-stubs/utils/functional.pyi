from typing import Any, Callable, List, Optional, Tuple, Type, Union

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields.array import ArrayField
from django.contrib.postgres.fields.hstore import HStoreField
from django.contrib.postgres.fields.jsonb import JSONField
from django.contrib.postgres.fields.ranges import (BigIntegerRangeField,
                                                   DateRangeField,
                                                   DateTimeRangeField,
                                                   FloatRangeField,
                                                   IntegerRangeField)
from django.contrib.postgres.search import SearchVectorField
from django.core.files.storage import FileSystemStorage
from django.core.handlers.wsgi import WSGIRequest
from django.core.management.commands.loaddata import Command
from django.core.paginator import Paginator
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.migrations.operations.fields import AlterField
from django.db.migrations.operations.models import RenameModel
from django.db.migrations.state import ModelState, ProjectState
from django.db.models.aggregates import Max, Min
from django.db.models.base import Model
from django.db.models.expressions import Col
from django.db.models.fields import (AutoField, BooleanField, CharField,
                                     DateTimeField, FloatField, IntegerField,
                                     TextField)
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.fields.related_descriptors import (ForwardManyToOneDescriptor,
                                                         ReverseOneToOneDescriptor)
from django.db.models.fields.related_lookups import RelatedIn
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.db.models.functions.datetime import Trunc
from django.db.models.lookups import (Exact, GreaterThanOrEqual, IExact,
                                      IsNull, LessThan)
from django.db.models.options import Options
from django.db.models.sql.query import Query
from django.db.models.sql.where import WhereNode
from django.db.utils import ConnectionHandler, ConnectionRouter
from django.forms.boundfield import BoundField
from django.forms.renderers import DjangoTemplates
from django.template.engine import Engine
from django.template.utils import EngineHandler
from django.urls.resolvers import URLResolver


def curry(_curried_func: Any, *args: Any, **kwargs: Any): ...

class cached_property:
    func: Callable = ...
    __doc__: Any = ...
    name: str = ...
    def __init__(self, func: Callable, name: None = ...) -> None: ...
    def __get__(
        self,
        instance: Any,
        cls: Type[
            Union[
                ProjectState,
                RenameModel,
                CharField,
                DatabaseWrapper,
                WSGIRequest,
                DateTimeRangeField,
                ModelState,
                TextField,
                Engine,
                ArrayField,
                related_descriptors.ForwardManyToOneDescriptor,
                JSONField,
                IsNull,
                BooleanField,
                DateRangeField,
                BoundField,
                URLResolver,
                reverse_related.ForeignObjectRel,
                WhereNode,
                EngineHandler,
                ConnectionHandler,
                GenericRelation,
                Query,
                Max,
                DjangoTemplates,
                HStoreField,
                IntegerField,
                IntegerRangeField,
                DateTimeField,
                ConnectionRouter,
                IExact,
                Exact,
                AutoField,
                Min,
                related.ManyToManyField,
                Command,
                AlterField,
                related.ForeignKey,
                BigIntegerRangeField,
                SearchVectorField,
                files.ImageField,
                related_descriptors.ReverseOneToOneDescriptor,
                GreaterThanOrEqual,
                FloatField,
                related_lookups.RelatedIn,
                Trunc,
                Col,
                LessThan,
                Options,
                Paginator,
                FileSystemStorage,
                FloatRangeField,
            ]
        ] = ...,
    ) -> Any: ...

class Promise: ...

def lazy(func: Callable, *resultclasses: Any) -> Callable: ...
def lazystr(text: Any): ...
def keep_lazy(*resultclasses: Any): ...
def keep_lazy_text(func: Any): ...

empty: Any

def new_method_proxy(func: Any): ...

class LazyObject:
    def __init__(self) -> None: ...
    __getattr__: Any = ...
    def __setattr__(self, name: str, value: Any) -> None: ...
    def __delattr__(self, name: Any) -> None: ...
    def __reduce__(self): ...
    def __copy__(self): ...
    def __deepcopy__(self, memo: Any): ...
    __bytes__: Any = ...
    __bool__: Any = ...
    __dir__: Any = ...
    __class__: Any = ...
    __eq__: Any = ...
    __ne__: Any = ...
    __hash__: Any = ...
    __getitem__: Any = ...
    __setitem__: Any = ...
    __delitem__: Any = ...
    __iter__: Any = ...
    __len__: Any = ...
    __contains__: Any = ...

def unpickle_lazyobject(wrapped: Any): ...

class SimpleLazyObject(LazyObject):
    def __init__(self, func: Callable) -> None: ...
    def __copy__(self): ...
    def __deepcopy__(self, memo: Any): ...

def partition(
    predicate: Callable, values: List[Model]
) -> Tuple[List[Model], List[Model]]: ...
