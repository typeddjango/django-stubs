from datetime import date, time, timedelta
from decimal import Context
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union
from uuid import UUID

from django.contrib.sessions.backends.db import SessionStore
from django.contrib.staticfiles.management.commands.collectstatic import \
    Command
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import File
from django.core.files.storage import FileSystemStorage
from django.core.management.base import BaseCommand
from django.core.management.commands.loaddata import Command
from django.core.management.commands.makemessages import BuildFile, Command
from django.core.paginator import Paginator
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.backends.sqlite3.features import DatabaseFeatures
from django.db.migrations.operations.base import Operation
from django.db.migrations.operations.fields import (AddField, AlterField,
                                                    RemoveField, RenameField)
from django.db.migrations.operations.models import (AlterIndexTogether,
                                                    AlterModelTable,
                                                    AlterOrderWithRespectTo,
                                                    AlterUniqueTogether,
                                                    CreateModel, DeleteModel,
                                                    RenameModel)
from django.db.migrations.state import ModelState, ProjectState, StateApps
from django.db.models.base import Model
from django.db.models.expressions import (BaseExpression, Col, Expression,
                                          OrderBy)
from django.db.models.fields import Field
from django.db.models.fields.files import FieldFile
from django.db.models.fields.mixins import FieldCacheMixin
from django.db.models.fields.related import RelatedField
from django.db.models.fields.related_descriptors import (ForwardManyToOneDescriptor,
                                                         ReverseOneToOneDescriptor)
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.db.models.lookups import Lookup
from django.db.models.manager import Manager
from django.db.models.options import Options
from django.db.models.query import QuerySet, RawQuerySet
from django.db.models.sql.query import Query
from django.db.models.sql.where import WhereNode
from django.db.utils import ConnectionHandler, ConnectionRouter
from django.forms.boundfield import BoundField, BoundWidget
from django.forms.forms import Form
from django.forms.renderers import DjangoTemplates, EngineMixin, Jinja2
from django.http.request import HttpRequest
from django.template.backends.base import BaseEngine
from django.template.backends.dummy import TemplateStrings
from django.template.backends.jinja2 import Jinja2
from django.template.engine import Engine
from django.template.loaders.base import Loader
from django.template.utils import EngineHandler
from django.urls.resolvers import URLPattern, URLResolver
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.dates import (ArchiveIndexView, DateDetailView,
                                        DayArchiveView, MonthArchiveView,
                                        TodayArchiveView, WeekArchiveView,
                                        YearArchiveView)


def curry(_curried_func: Any, *args: Any, **kwargs: Any): ...

class cached_property:
    func: Callable = ...
    __doc__: Any = ...
    name: str = ...
    def __init__(self, func: Callable, name: Optional[str] = ...) -> None: ...
    def __get__(
        self,
        instance: Optional[
            Union[
                SessionStore,
                File,
                FileSystemStorage,
                BaseCommand,
                BuildFile,
                Paginator,
                DatabaseWrapper,
                DatabaseFeatures,
                Operation,
                ModelState,
                ProjectState,
                BaseExpression,
                Field,
                ForwardManyToOneDescriptor,
                ReverseOneToOneDescriptor,
                ForeignObjectRel,
                Lookup,
                Options,
                RawQuerySet,
                Query,
                WhereNode,
                ConnectionHandler,
                ConnectionRouter,
                BoundField,
                Form,
                EngineMixin,
                HttpRequest,
                BaseEngine,
                Engine,
                EngineHandler,
                URLPattern,
                URLResolver,
                TemplateResponseMixin,
            ]
        ],
        cls: Type[
            Union[
                SessionStore,
                Command,
                File,
                FileSystemStorage,
                Command,
                BuildFile,
                Command,
                Paginator,
                DatabaseWrapper,
                DatabaseFeatures,
                AddField,
                AlterField,
                RemoveField,
                RenameField,
                AlterIndexTogether,
                AlterModelTable,
                AlterOrderWithRespectTo,
                AlterUniqueTogether,
                CreateModel,
                DeleteModel,
                RenameModel,
                ModelState,
                ProjectState,
                Model,
                Expression,
                OrderBy,
                Field,
                ForwardManyToOneDescriptor,
                ReverseOneToOneDescriptor,
                ForeignObjectRel,
                Lookup,
                Options,
                RawQuerySet,
                Query,
                WhereNode,
                ConnectionHandler,
                ConnectionRouter,
                BoundField,
                Form,
                DjangoTemplates,
                Jinja2,
                HttpRequest,
                TemplateStrings,
                Jinja2,
                Engine,
                EngineHandler,
                URLPattern,
                URLResolver,
                ArchiveIndexView,
                DateDetailView,
                DayArchiveView,
                MonthArchiveView,
                TodayArchiveView,
                WeekArchiveView,
                YearArchiveView,
            ]
        ] = ...,
    ) -> Optional[
        Union[
            Callable,
            Dict[str, Dict[str, Union[Dict[str, bool], str]]],
            Dict[str, Dict[str, Union[Dict[str, str], str]]],
            Dict[str, Union[Field, mixins.FieldCacheMixin, str]],
            Dict[str, Manager],
            List[Tuple[str, Callable]],
            List[Union[Callable, related.RelatedField]],
            List[Union[BoundWidget, Loader]],
            List[Union[URLPattern, URLResolver]],
            List[Union[int, str]],
            List[Model],
            Tuple,
            Type[Union[Any, ObjectDoesNotExist, Model, str]],
            date,
            time,
            timedelta,
            Context,
            StateApps,
            Model,
            Col,
            Field,
            files.FieldFile,
            Manager,
            QuerySet,
            BaseEngine,
            cached_property,
            float,
            frozenset,
            int,
            str,
            UUID,
        ]
    ]: ...

class Promise: ...

def lazy(func: Union[Callable, Type[str]], *resultclasses: Any) -> Callable: ...
def lazystr(text: Any): ...
def keep_lazy(*resultclasses: Any) -> Callable: ...
def keep_lazy_text(func: Callable) -> Callable: ...

empty: Any

def new_method_proxy(func: Any): ...

class LazyObject:
    def __init__(self) -> None: ...
    __getattr__: Any = ...
    def __setattr__(self, name: str, value: Any) -> None: ...
    def __delattr__(self, name: str) -> None: ...
    def __reduce__(self) -> Tuple[Callable, Tuple[Model]]: ...
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

def unpickle_lazyobject(wrapped: Model) -> Model: ...

class SimpleLazyObject(LazyObject):
    def __init__(self, func: Callable) -> None: ...
    def __copy__(self) -> List[int]: ...
    def __deepcopy__(self, memo: Dict[Any, Any]) -> List[int]: ...

def partition(
    predicate: Callable, values: List[Model]
) -> Tuple[List[Model], List[Model]]: ...
