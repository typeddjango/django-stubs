<img src="http://mypy-lang.org/static/mypy_light.svg" alt="mypy logo" width="300px"/>

# pep484 stubs for Django

[![Build Status](https://travis-ci.com/typeddjango/django-stubs.svg?branch=master)](https://travis-ci.com/typeddjango/django-stubs)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Gitter](https://badges.gitter.im/mypy-django/Lobby.svg)](https://gitter.im/mypy-django/Lobby)


This package contains [type stubs](https://www.python.org/dev/peps/pep-0561/) and a custom mypy plugin to provide more precise static types and type inference for Django framework. Django uses some Python "magic" that makes having precise types for some code patterns problematic. This is why we need this project. The final goal is to be able to get precise types for most common patterns.


## Installation

```bash
pip install django-stubs
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

Two things happeining here:

1. We need to explicitly list our plugin to be loaded by `mypy`
2. Our plugin also requires `django` settings module (what you put into `DJANGO_SETTINGS_MODULE` variable) to be specified

This fully working [typed boilerplate](https://github.com/wemake-services/wemake-django-template) can serve you as an example.

## Version compatibility

We rely on different `django` and `mypy` versions:

| django-stubs | mypy version | django version | python version
| ------------ | ---- | ---- | ---- |
| 1.6.0 | 0.780 | 2.2.x \|\| 3.x | ^3.6
| 1.5.0 | 0.770 | 2.2.x \|\| 3.x | ^3.6
| 1.4.0 | 0.760 | 2.2.x \|\| 3.x | ^3.6
| 1.3.0 | 0.750 | 2.2.x \|\| 3.x | ^3.6
| 1.2.0 | 0.730 | 2.2.x | ^3.6
| 1.1.0 | 0.720 | 2.2.x | ^3.6
| 0.12.x | old semantic analyzer (<0.711), dmypy support | 2.1.x | ^3.6


## FAQ

### Is this an official Django project?

No, it is not. We are independent from Django at the moment.
There's a [proposal](https://github.com/django/deps/pull/65) to merge our project into the Django itself.
You show your support by linking the PR.

### Is it safe to use this in production?

Yes, it is! This project does not affect your runtime at all.
It only affects `mypy` type checking process.

But, it does not make any sense to use this project without `mypy`.

### mypy crashes when I run it with this plugin installed

Current implementation uses Django runtime to extract models information, so it will crash, if your installed apps or `models.py` is not correct. For this same reason, you cannot use `reveal_type` inside global scope of any Python file that will be executed for `django.setup()`.

In other words, if your `manage.py runserver` crashes, mypy will crash too.
You can also run `mypy` with [`--tb`](https://mypy.readthedocs.io/en/stable/command_line.html#cmdoption-mypy-show-traceback)
option to get extra information about the error.

### I cannot use QuerySet or Manager with type annotations

You can get a `TypeError: 'type' object is not subscriptable`
when you will try to use `QuerySet[MyModel]` or `Manager[MyModel]`.

This happens because Django classes do not support [`__class_getitem__`](https://www.python.org/dev/peps/pep-0560/#class-getitem) magic method.

You can use strings instead: `'QuerySet[MyModel]'` and `'Manager[MyModel]'`, this way it will work as a type for `mypy` and as a regular `str` in runtime.

Currently we [are working](https://github.com/django/django/pull/12405) on providing `__class_getitem__` to the classes where we need them.

### How can I create a HttpRequest that's guaranteed to have an authenticated user?

Django's built in `HttpRequest` has the attribute `user` that resolves to the type
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

You can always also reach out in gitter to discuss your contributions!
