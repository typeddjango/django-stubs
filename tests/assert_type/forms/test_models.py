from typing import cast

from django.db.models import Model, QuerySet
from django.forms.models import InlineForeignKeyField, ModelChoiceField, ModelMultipleChoiceField
from django.forms.widgets import Widget
from typing_extensions import assert_type


class TestModel(Model): ...


testmodel_instance = cast(TestModel, ...)

assert_type(InlineForeignKeyField.widget, type[Widget] | Widget)
assert_type(InlineForeignKeyField(testmodel_instance).widget, Widget)

testmodel_queryset = cast(QuerySet[TestModel], ...)

assert_type(ModelChoiceField.widget, type[Widget] | Widget)
assert_type(ModelChoiceField(testmodel_queryset).widget, Widget)

assert_type(ModelMultipleChoiceField.widget, type[Widget] | Widget)
assert_type(ModelMultipleChoiceField(testmodel_queryset).widget, Widget)
