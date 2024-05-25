<img src="https://raw.githubusercontent.com/typeddjango/django-stubs/master/logo.svg" alt="django-stubs">

[![Build status](https://github.com/typeddjango/django-stubs/workflows/test/badge.svg?branch=master&event=push)](https://github.com/typeddjango/django-stubs/actions?query=workflow%3Atest)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Gitter](https://badges.gitter.im/mypy-django/Lobby.svg)](https://gitter.im/mypy-django/Lobby)
[![StackOverflow](https://shields.io/badge/ask-stackoverflow-orange?logo=stackoverflow)](https://stackoverflow.com/questions/tagged/django-stubs)

This package contains [type stubs](https://www.python.org/dev/peps/pep-0561/) and a custom mypy plugin to provide more precise static types and type inference for Django framework. Django uses some Python "magic" that makes having precise types for some code patterns problematic. This is why we need this project. The final goal is to be able to get precise types for most common patterns.

## Installation

```bash
pip install django-stubs[compatible-mypy]
```

To make mypy aware of the plugin, you need to add

```ini
[mypy]
plugins =
    mypy_django_plugin.main

[mypy.plugins.django-stubs]
django_settings_module = "myproject.settings"
```

in your `mypy.ini` or `setup.cfg` [file](https://mypy.readthedocs.io/en/latest/config_file.html).

[pyproject.toml](https://mypy.readthedocs.io/en/stable/config_file.html#using-a-pyproject-toml-file) configurations are also supported:

```toml
[tool.mypy]
plugins = ["mypy_django_plugin.main"]

[tool.django-stubs]
django_settings_module = "myproject.settings"
```

Two things happening here:

1. We need to explicitly list our plugin to be loaded by `mypy`
2. You can either specify `django_settings_module` as seen above, or let `django_stubs` use the `DJANGO_SETTINGS_MODULE` variable from your environment.

This fully working [typed boilerplate](https://github.com/wemake-services/wemake-django-template) can serve you as an example.

## Version compatibility

We rely on different `django` and `mypy` versions:

| django-stubs   | Mypy version | Django version | Django partial support | Python version |
|----------------|--------------|----------------|------------------------|----------------|
| 5.0.1          | 1.10.x       | 5.0            | 4.2                    | 3.8 - 3.12     |
| 5.0.0          | 1.10.x       | 5.0            | 4.2, 4.1               | 3.8 - 3.12     |
| 4.2.7          | 1.7.x        | 4.2            | 4.1, 3.2               | 3.8 - 3.12     |
| 4.2.6          | 1.6.x        | 4.2            | 4.1, 3.2               | 3.8 - 3.12     |
| 4.2.5          | 1.6.x        | 4.2            | 4.1, 3.2               | 3.8 - 3.12     |
| 4.2.4          | 1.5.x        | 4.2            | 4.1, 3.2               | 3.8 - 3.11     |
| 4.2.3          | 1.4.x        | 4.2            | 4.1, 3.2               | 3.8 - 3.11     |
| 4.2.2          | 1.4.x        | 4.2            | 4.1, 3.2               | 3.8 - 3.11     |
| 4.2.1          | 1.3.x        | 4.2            | 4.1, 3.2               | 3.8 - 3.11     |
| 4.2.0          | 1.2.x        | 4.2            | 4.1, 4.0, 3.2          | 3.7 - 3.11     |
| 1.16.0         | 1.1.x        | 4.1            | 4.0, 3.2               | 3.7 - 3.11     |
| 1.15.0         | 1.0.x        | 4.1            | 4.0, 3.2               | 3.7 - 3.11     |
| 1.14.0         | 0.990+       | 4.1            | 4.0, 3.2               | 3.7 - 3.11     |

## Features

### Type checking of Model Meta attributes

By inheriting from the `TypedModelMeta` class, you can ensure you're using correct types for
attributes:

```python
from django.db import models
from django_stubs_ext.db.models import TypedModelMeta

class MyModel(models.Model):
    example = models.CharField(max_length=100)

    class Meta(TypedModelMeta):
        ordering = ["example"]
        constraints = [
            models.UniqueConstraint(fields=["example"], name="unique_example"),
        ]
```

### Other typed base classes

* `django_stubs_ext.db.router.TypedDatabaseRouter` can be used as base when implementing custom database routers.

## Settings

django-stubs has a few settings, which you can list in:

* `pyproject.toml`, under the table `[tool.django-stubs]`
* `mypy.ini` under the table `[mypy.plugins.django-stubs]`

The supported settings are:

- `django_settings_module`, a string, default to `os.getenv(DJANGO_SETTINGS_MODULE)`.

  Specify the import path of your settings module, the same as Django’s [`DJANGO_SETTINGS_MODULE` environment variable](https://docs.djangoproject.com/en/stable/topics/settings/#designating-the-settings).

- `strict_settings`, a boolean, default `true`.

  Set to `false` if using dynamic settings, as [described below](https://github.com/typeddjango/django-stubs#how-to-use-a-custom-library-to-handle-django-settings).

## FAQ

### Is this an official Django project?

No, it is not. We are independent from Django at the moment.
There's a [proposal](https://github.com/django/deps/pull/65) to merge our project into the Django itself.
You can show your support by liking the PR.

### Is it safe to use this in production?

Yes, it is! This project does not affect your runtime at all.
It only affects `mypy` type checking process.

But, it does not make any sense to use this project without `mypy`.

### mypy crashes when I run it with this plugin installed

The current implementation uses Django's runtime to extract information about models, so it might crash if your installed apps or `models.py` are broken.

In other words, if your `manage.py runserver` crashes, mypy will crash too.
You can also run `mypy` with [`--tb`](https://mypy.readthedocs.io/en/stable/command_line.html#cmdoption-mypy-show-traceback)
option to get extra information about the error.

### I cannot use QuerySet or Manager with type annotations

You can get a `TypeError: 'type' object is not subscriptable`
when you will try to use `QuerySet[MyModel]`, `Manager[MyModel]` or some other Django-based Generic types.

This happens because these Django classes do not support [`__class_getitem__`](https://www.python.org/dev/peps/pep-0560/#class-getitem) magic method in runtime.

1. You can go with our [`django_stubs_ext`](https://github.com/typeddjango/django-stubs/tree/master/ext) helper, that patches all the types we use as Generic in django.

   Install it:

   ```bash
   pip install django-stubs-ext  # as a production dependency
   ```

   And then place in your top-level settings:

   ```python
   import django_stubs_ext

   django_stubs_ext.monkeypatch()
   ```

   You can add extra types to patch with `django_stubs_ext.monkeypatch(extra_classes=[YourDesiredType])`

2. You can use strings instead: `'QuerySet[MyModel]'` and `'Manager[MyModel]'`, this way it will work as a type for `mypy` and as a regular `str` in runtime.

### How can I create a HttpRequest that's guaranteed to have an authenticated user?

Django's built in [`HttpRequest`](https://docs.djangoproject.com/en/4.1/ref/request-response/#django.http.HttpRequest) has the attribute `user` that resolves to the type

```python
Union[User, AnonymousUser]
```

where `User` is the user model specified by the `AUTH_USER_MODEL` setting.

If you want a `HttpRequest` that you can type-annotate with where you know that the user is authenticated you can subclass the normal `HttpRequest` class like so:

```python
from django.http import HttpRequest
from my_user_app.models import MyUser


class AuthenticatedHttpRequest(HttpRequest):
    user: MyUser
```

And then use `AuthenticatedHttpRequest` instead of the standard `HttpRequest` for when you know that the user is authenticated. For example in views using the `@login_required` decorator.

### Why am I getting incompatible return type errors on my custom managers?

If you declare your custom managers without generics and override built-in
methods you might see an error message about incompatible error messages,
something like this:

```python
from django.db import models

class MyManager(model.Manager):
    def create(self, **kwargs) -> "MyModel":
        pass
```

will cause this error message:

> error: Return type "MyModel" of "create" incompatible with return type "_T" in supertype "BaseManager"

This is happening because the `Manager` class is generic, but without
specifying generics the built-in manager methods are expected to return the
generic type of the base manager, which is any model. To fix this issue you
should declare your manager with your model as the type variable:

```python
class MyManager(models.Manager["MyModel"]):
    ...
```

### How do I annotate cases where I called QuerySet.annotate?

Django-stubs provides a special type, `django_stubs_ext.WithAnnotations[Model]`, which indicates that the `Model` has
been annotated, meaning it allows getting/setting extra attributes on the model instance.

Optionally, you can provide a `TypedDict` of these attributes,
e.g. `WithAnnotations[MyModel, MyTypedDict]`, to specify which annotated attributes are present.

Currently, the mypy plugin can recognize that specific names were passed to `QuerySet.annotate` and
include them in the type, but does not record the types of these attributes.

The knowledge of the specific annotated fields is not yet used in creating more specific types for `QuerySet`'s
`values`, `values_list`, or `filter` methods, however knowledge that the model was annotated _is_ used to create a
broader type result type for `values`/`values_list`, and to allow `filter`ing on any field.

```python
from typing import TypedDict
from django_stubs_ext import WithAnnotations
from django.db import models
from django.db.models.expressions import Value


class MyModel(models.Model):
    username = models.CharField(max_length=100)


def func(m: WithAnnotations[MyModel]) -> str:
    return m.asdf  # OK, since the model is annotated as allowing any attribute


func(MyModel.objects.annotate(foo=Value("")).get(id=1))  # OK
func(
    MyModel.objects.get(id=1)
)  # Error, since this model will not allow access to any attribute


class MyTypedDict(TypedDict):
    foo: str


def func2(m: WithAnnotations[MyModel, MyTypedDict]) -> str:
    print(m.bar)  # Error, since field "bar" is not in MyModel or MyTypedDict.
    return m.foo  # OK, since we said field "foo" was allowed


func(MyModel.objects.annotate(foo=Value("")).get(id=1))  # OK
func(MyModel.objects.annotate(bar=Value("")).get(id=1))  # Error
```

### Why am I getting incompatible argument type mentioning `_StrPromise`?

The lazy translation functions of Django (such as `gettext_lazy`) return a `Promise` instead of `str`. These two types [cannot be used interchangeably](https://github.com/typeddjango/django-stubs/pull/1139#issuecomment-1232167698). The return type of these functions was therefore [changed](https://github.com/typeddjango/django-stubs/pull/689) to reflect that.

If you encounter this error in your own code, you can either cast the `Promise` to `str` (causing the translation to be evaluated), or use the `StrPromise` or `StrOrPromise` types from `django-stubs-ext` in type hints. Which solution to choose depends depends on the particular case. See [working with lazy translation objects](https://docs.djangoproject.com/en/4.1/topics/i18n/translation/#working-with-lazy-translation-objects) in the Django documentation for more information.

If this is reported on Django code, please report an issue or open a pull request to fix the type hints.

### How to use a custom library to handle Django settings?

Using something like [`django-split-settings`](https://github.com/wemake-services/django-split-settings) or [`django-configurations`](https://github.com/jazzband/django-configurations) will make it hard for mypy to infer your settings.

This might also be the case when using something like:

```python
try:
    from .local_settings import *
except Exception:
    pass
```

So, mypy would not like this code:

```python
from django.conf import settings

settings.CUSTOM_VALUE  # E: 'Settings' object has no attribute 'CUSTOM_VALUE'
```

To handle this corner case we have a special setting `strict_settings` (`True` by default),
you can switch it to `False` to always return `Any` and not raise any errors if runtime settings module has the given value,
for example `pyproject.toml`:

```toml
[tool.django-stubs]
strict_settings = false
```

or `mypy.ini`:

```ini
[mypy.plugins.django-stubs]
strict_settings = false
```

And then:

```python
# Works:
reveal_type(settings.EXISTS_AT_RUNTIME)  # N: Any

# Errors:
reveal_type(settings.MISSING)  # E: 'Settings' object has no attribute 'MISSING'
```

## Related projects

- [`awesome-python-typing`](https://github.com/typeddjango/awesome-python-typing) - Awesome list of all typing-related things in Python.
- [`djangorestframework-stubs`](https://github.com/typeddjango/djangorestframework-stubs) - Stubs for Django REST Framework.
- [`pytest-mypy-plugins`](https://github.com/typeddjango/pytest-mypy-plugins) - `pytest` plugin that we use for testing `mypy` stubs and plugins.
- [`wemake-django-template`](https://github.com/wemake-services/wemake-django-template) - Create new typed Django projects in seconds.

## To get help

We have Gitter here: <https://gitter.im/mypy-django/Lobby>
If you think you have more generic typing issue, please refer to <https://github.com/python/mypy> and their Gitter.

## Contributing

This project is open source and community driven. As such we encourage contributions big and small. You can contribute by doing any of the following:

1. Contribute code (e.g. improve stubs, add plugin capabilities, write tests etc) - to do so please follow the [contribution guide](./CONTRIBUTING.md).
2. Assist in code reviews and discussions in issues.
3. Identify bugs and issues and report these
4. Ask and answer questions on [StackOverflow](https://stackoverflow.com/questions/tagged/django-stubs)

You can always also reach out in gitter to discuss your contributions!
