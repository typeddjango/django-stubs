<img src="http://mypy-lang.org/static/mypy_light.svg" alt="mypy logo" width="300px"/>

# pep484 stubs for Django framework

[![Build Status](https://travis-ci.org/mkurnikov/django-stubs.svg?branch=master)](https://travis-ci.org/mkurnikov/django-stubs)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

This package contains type stubs and mypy plugin to provide more precise static types and type inference for Django framework. Django uses some Python "magic" that makes having precise types for some code patterns problematic. This is why we need to accompany the stubs with mypy plugins. The final goal is to be able to get precise types for most common patterns.

Supports Python 3.6/3.7, and Django 2.1.x series.

Could be run on earlier versions of Django, but expect some missing imports warnings.

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


## Configuration

In order to specify config file, set `MYPY_DJANGO_CONFIG` environment variable with path to the config file. Default is `./mypy_django.ini`

Config file format (.ini):
```
[mypy_django_plugin]

# specify settings module to use for django.conf.settings, this setting
# could also be specified with DJANGO_SETTINGS_MODULE environment variable
# (it also takes priority over config file)
django_settings = mysettings.local

# if True, all unknown settings in django.conf.settings will fallback to Any,
# specify it if your settings are loaded dynamically to avoid false positives
ignore_missing_settings = True
```

## To get help

We have Gitter here https://gitter.im/mypy-django/Lobby.

If you think you have more generic typing issue, please refer to https://github.com/python/mypy and their Gitter.