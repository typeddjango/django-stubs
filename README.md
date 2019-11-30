<img src="http://mypy-lang.org/static/mypy_light.svg" alt="mypy logo" width="300px"/>

# pep484 stubs for Django framework

[![Build Status](https://travis-ci.com/typeddjango/django-stubs.svg?branch=master)](https://travis-ci.com/typeddjango/django-stubs)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Gitter](https://badges.gitter.im/mypy-django/Lobby.svg)](https://gitter.im/mypy-django/Lobby)

This package contains type stubs and mypy plugin to provide more precise static types and type inference for Django framework. Django uses some Python "magic" that makes having precise types for some code patterns problematic. This is why we need to accompany the stubs with mypy plugins. The final goal is to be able to get precise types for most common patterns.

Could be run on earlier versions of Django, but expect some missing imports warnings.


## Installation

```bash
pip install django-stubs
```


## Mypy compatibility

| django-stubs | mypy version | django version | python version
| ------------ | ---- | ---- | ---- |
| 1.3.0 | 0.750 | 2.2.x | ^3.6
| 1.2.0 | 0.730 | 2.2.x | ^3.6
| 1.1.0 | 0.720 | 2.2.x | ^3.6
| 0.12.x | old semantic analyzer (<0.711), dmypy support | 2.1.x | ^3.6


## Configuration

To make mypy aware of the plugin, you need to add

```ini
[mypy]
plugins =
    mypy_django_plugin.main
```

in your `mypy.ini` or `setup.cfg` [file](https://mypy.readthedocs.io/en/latest/config_file.html).

Plugin also requires Django settings module (what you put into `DJANGO_SETTINGS_MODULE` variable) to be specified.

```ini
[mypy]
strict_optional = True

# This one is new:
[mypy.plugins.django-stubs]
django_settings_module = mysettings
```

Where `mysettings` is a value of `DJANGO_SETTINGS_MODULE` (with or without quotes)

Current implementation uses Django runtime to extract models information, so it will crash, if your installed apps `models.py` is not correct. For this same reason, you cannot use `reveal_type` inside global scope of any Python file that will be executed for `django.setup()`. 

In other words, if your `manage.py runserver` crashes, mypy will crash too. 

This fully working [typed boilerplate](https://github.com/wemake-services/wemake-django-template) can serve you as an example.


## Notes

Type implementation monkey-patches Django to add `__class_getitem__` to the `Manager` class. 
If you would use Python3.7 and do that too in your code, you can make things like

```python
class MyUserManager(models.Manager['MyUser']):
    pass

class MyUser(models.Model):
    objects = MyUserManager()
```

work, which should make a error messages a bit better. 

Otherwise, custom type will be created in mypy, named `MyUser__MyUserManager`, which will rewrite base manager as `models.Manager[User]` to make methods like `get_queryset()` and others return properly typed `QuerySet`. 


## To get help

We have Gitter here: <https://gitter.im/mypy-django/Lobby>

If you think you have more generic typing issue, please refer to https://github.com/python/mypy and their Gitter.
