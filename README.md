[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/mypy-django/Lobby)

# django-stubs

The aim of this project is to bring [PEP 484 type hints] to Django.

We currently focus on supporting Django >= 2.1 to simplify work in the beginning.

[PEP 484 type hints]: https://www.python.org/dev/peps/pep-0484/

## The Plan

  * Use [retype]/[MonkeyType]/[stubgen] to auto-generate [django-stubs] Django 2.1.
  * Integrate [machinalis/mypy-django] stubs into [django-stubs].
  * Create a [mypy plugin] to support Django model dynamic behaviour. See [django-stubs/#5] for more.
  * Create a test-suite to keep synced with upstream Django. See [django-stubs/#3] for more.
  * Commence refining auto-generated stubs and plugin until it is useful.
  * Start conversation with Django core about potential integration.

This plan is not set in stone and can change.

[django-stubs]: https://github.com/TypedDjango/django-stubs
[retype]: https://github.com/ambv/retype
[MonkeyType]: https://github.com/Instagram/MonkeyType
[stubgen]: https://github.com/python/mypy/blob/master/mypy/stubgen.py
[machinalis/mypy-django]: https://github.com/machinalis/mypy-django
[django-stubs/#3]: https://github.com/TypedDjango/django-stubs/issues/3
[mypy plugin]: https://github.com/python/mypy/tree/master/mypy/plugins
[django-stubs/#5]: https://github.com/TypedDjango/django-stubs/issues/5

## Join Us

Bringing type hints to Django will be a huge achievement but will require *a
lot* of work. It is still unclear as to how much time and effort but one thing
is clear: we will need a lot of help. No matter what skill level or amount of
free time, if you have some motivation to help, please do so.

Right now, the best way to start helping is:

  * Introduce yourself on the [Gitter chat room].
  * Start picking up one of [the issues].
  * Review and help triage the [project management board].

[Gitter chat room]: https://gitter.im/mypy-django/Lobby
[the issues]: https://github.com/TypedDjango/django-stubs/issues
[project management board]: https://github.com/orgs/TypedDjango/projects/1

## Other Django Stub Efforts

We'll hopefully merge these existing efforts here as we move along.

  * https://github.com/machinalis/mypy-django
  * https://github.com/facebook/pyre-check/tree/master/stubs/3/django
  * https://github.com/zulip/zulip/issues/991
  * https://gitlab.com/melvyn-sopacua/typeshed/commits/django

## How was django-stubs initially auto-generated?

The initial work was done by [@mkurnikov] and will be documented once [django-stubs/#2] is done.

[@mkurnikov]: https://github.com/mkurnikov
[django-stubs/#2]: https://github.com/TypedDjango/django-stubs/issues/2
