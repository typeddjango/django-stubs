from __future__ import annotations

from typing import assert_type

from django import forms
from django.db import models
from django.db.models import F
from django.db.models.functions import Upper
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView


class MyModel(models.Model): ...


class MyDetailView(SingleObjectMixin[MyModel]): ...


detail_view = MyDetailView()
assert_type(detail_view.model, type[MyModel])
assert_type(detail_view.queryset, models.QuerySet[MyModel, MyModel] | None)
assert_type(detail_view.get_context_object_name(MyModel()), str)
assert_type(detail_view.get_context_object_name(1), str | None)


class MyListView(ListView[MyModel]): ...


list_view = MyListView()
assert_type(list_view.model, type[MyModel] | None)
assert_type(list_view.queryset, models.QuerySet[MyModel, MyModel] | None)
assert_type(list_view.get_context_object_name(models.QuerySet[MyModel]()), str)
assert_type(list_view.get_context_object_name(MyModel()), str | None)
assert_type(list_view.get_context_object_name(1), str | None)


class ConfirmForm(forms.Form): ...


class MyDeleteView(DeleteView[MyModel, ConfirmForm]): ...


delete_view = MyDeleteView()
assert_type(delete_view.get_form_class(), type[ConfirmForm])
assert_type(delete_view.get_form(), ConfirmForm)


# When no form type parameter is given, the form types default to what Django provides at runtime.
class SimpleCreateView(CreateView[MyModel]):
    model = MyModel
    fields = "__all__"


simple_create_view = SimpleCreateView()
assert_type(simple_create_view.get_form_class(), type[forms.ModelForm[MyModel]])
assert_type(simple_create_view.get_form(), forms.ModelForm[MyModel])


class SimpleUpdateView(UpdateView[MyModel]):
    model = MyModel
    fields = "__all__"


simple_update_view = SimpleUpdateView()
assert_type(simple_update_view.get_form_class(), type[forms.ModelForm[MyModel]])
assert_type(simple_update_view.get_form(), forms.ModelForm[MyModel])


class SimpleDeleteView(DeleteView[MyModel]):
    model = MyModel


simple_delete_view = SimpleDeleteView()
assert_type(simple_delete_view.get_form_class(), type[forms.Form])
assert_type(simple_delete_view.get_form(), forms.Form)


class MyOrderedListView(ListView[MyModel]):
    ordering = [Upper("id")]


class MyMixedOrderingListView(ListView[MyModel]):
    ordering = ["-id", F("id").asc()]
