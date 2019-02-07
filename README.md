<img src="http://mypy-lang.org/static/mypy_light.svg" alt="mypy logo" width="300px"/>

# pep484 stubs for Django framework

[![Build Status](https://travis-ci.org/mkurnikov/django-stubs.svg?branch=master)](https://travis-ci.org/mkurnikov/django-stubs)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

This package contains type stubs and mypy plugin to provide more precise static types and type inference for Django framework. Django uses some Python "magic" that makes having precise types for some code patterns problematic. This is why we need to accompany the stubs with mypy plugins. The final goal is to be able to get precise types for most common patterns.

## Installation

```
pip install django-stubs
```

To make mypy aware of the plugin, you need to add

```
[mypy]
plugins =
    mypy_django_plugin.main
```

in your `mypy.ini` file.


### `django.conf.settings` support

`settings.SETTING_NAME` will only work if `DJANGO_SETTINGS_MODULE` will be present in the environment, when mypy is executed.

If some setting is not recognized to the plugin, but it's clearly there, try adding type annotation to it.


## To get help

We have Gitter here https://gitter.im/mypy-django/Lobby.

If you think you have more generic typing issue, please refer to https://github.com/python/mypy and their Gitter.