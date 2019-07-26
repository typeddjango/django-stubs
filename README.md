<img src="http://mypy-lang.org/static/mypy_light.svg" alt="mypy logo" width="300px"/>

# pep484 stubs for Django framework

[![Build Status](https://travis-ci.org/mkurnikov/django-stubs.svg?branch=master)](https://travis-ci.org/mkurnikov/django-stubs)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

This package contains type stubs and mypy plugin to provide more precise static types and type inference for Django framework. Django uses some Python "magic" that makes having precise types for some code patterns problematic. This is why we need to accompany the stubs with mypy plugins. The final goal is to be able to get precise types for most common patterns.

Supports Python 3.6/3.7, and Django 2.1/2.2.

Could be run on earlier versions of Django, but expect some missing imports warnings.

## Installation

```
pip install django-stubs
```

### WARNING: All configuration from pre-1.0.0 versions is dropped, use one below.

### WARNING: 1.0.0 breaks `dmypy`, if you need it, stay on the 0.12.x series. 

To make mypy aware of the plugin, you need to add

```
[mypy]
plugins =
    mypy_django_plugin.main
```

in your `mypy.ini` file.

Plugin requires Django settings module (what you put into `DJANGO_SETTINGS_MODULE` variable) to be specified inside `mypy.ini` file.
```
[mypy]
strict_optional = True

; this one is new
[mypy.plugins.django-stubs]
django_settings_module = mysettings
```
where `mysettings` is a value of `DJANGO_SETTINGS_MODULE` (with or without quotes)

Do you have trouble with mypy / the django plugin not finding your settings module? Try adding the root path of your project to your PYTHONPATH environment variable. If you use pipenv you can add the following to an `.env` file in your project root which pipenv will run automatically before executing any commands.:
```
PYTHONPATH=${PYTHONPATH}:${PWD}
```

New implementation uses Django runtime to extract models information, so it will crash, if your installed apps `models.py` is not correct. For this same reason, you cannot use `reveal_type` inside global scope of any Python file that will be executed for `django.setup()`. 

In other words, if your `manage.py runserver` crashes, mypy will crash too. 

## Notes

Implementation monkey-patches Django to add `__class_getitem__` to the `Manager` class. If you'd use Python3.7 and do that too in your code, you can make things like
```
class MyUserManager(models.Manager['MyUser']):
    pass
class MyUser(models.Model):
    objects = UserManager()
```
work, which should make a error messages a bit better. 

Otherwise, custom type will be created in mypy, named `MyUser__MyUserManager`, which will rewrite base manager as `models.Manager[User]` to make methods like `get_queryset()` and others return properly typed `QuerySet`. 

## To get help

We have Gitter here https://gitter.im/mypy-django/Lobby.

If you think you have more generic typing issue, please refer to https://github.com/python/mypy and their Gitter.
