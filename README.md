<img src="http://mypy-lang.org/static/mypy_light.svg" alt="mypy logo" width="300px"/>

# pep484 stubs for Django framework

[![Build Status](https://travis-ci.org/mkurnikov/django-stubs.svg?branch=master)](https://travis-ci.org/mkurnikov/django-stubs)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

This package contains type stubs and mypy plugin to provide more precise static types and type inference for Django framework. Django uses some Python "magic" that makes having precise types for some code patterns problematic. This is why we need to accompany the stubs with mypy plugins. The final goal is to be able to get precise types for most common patterns.

## Installation

```
git clone https://github.com/mkurnikov/django-stubs.git
cd django-stubs
pip install -U .
```

To make mypy aware of the plugin, you need to add

```
[mypy]
plugins =
    mypy_django_plugin.main
```

in your `mypy.ini` file.

Also, it uses value of `DJANGO_SETTINGS_MODULE` from the environment, so set it before execution, otherwise some features will not work.