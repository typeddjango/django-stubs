# django-types [![PyPI](https://img.shields.io/pypi/v/django-types.svg)](https://pypi.org/project/django-types/)

Type stubs for [Django](https://www.djangoproject.com).

> Note: this project was forked from
> <https://github.com/typeddjango/django-stubs> with the goal of removing the
> [`mypy`](https://github.com/python/mypy) plugin dependency so that `mypy`
> can't [crash due to Django
> config](https://github.com/typeddjango/django-stubs/issues/318), and that
> non-`mypy` type checkers like
> [`pyright`](https://github.com/microsoft/pyright) will work better with
> Django.

## install

```bash
pip install django-types
```

You'll need to monkey patch Django's `QuerySet`, `Manager` (not needed for Django 3.1+) and
`ForeignKey` classes so we can index into them with a generic argument. Add this to your
settings.py:

```python
# in settings.py
from django.db.models import ForeignKey
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet

# NOTE: there are probably other items you'll need to monkey patch depending on
# your version.
for cls in [QuerySet, BaseManager, ForeignKey]:
    cls.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls)  # type: ignore [attr-defined]
```

## usage

### ForeignKey ids and related names as properties in ORM models

When defining a Django ORM model with a foreign key, like so:

```python
class User(models.Model):
    team = models.ForeignKey(
        "Team",
        null=True,
        on_delete=models.SET_NULL,
    )
    role = models.ForeignKey(
        "Role",
        null=True,
        on_delete=models.SET_NULL,
        related_name="users",
    )
```

two properties are created, `team` as expected, and `team_id`. Also, a related
manager called `user_set` is created on `Team` for the reverse access.

In order to properly add typing to the foreing key itself and also for the created ids you can do
something like this:

```python
from typing import TYPE_CHECKING

from someapp.models import Team
if TYPE_CHECKING:
    # In this example Role cannot be imported due to circular import issues,
    # but doing so inside TYPE_CHECKING will make sure that the typing bellow
    # knows what "Role" means
    from anotherapp.models import Role


class User(models.Model):
    team_id: Optional[int]
    team = models.ForeignKey(
        Team,
        null=True,
        on_delete=models.SET_NULL,
    )
    role_id: int
    role = models.ForeignKey["Role"](
        "Role",
        null=False,
        on_delete=models.SET_NULL,
        related_name="users",
    )


reveal_type(User().team)
# note: Revealed type is 'Optional[Team]'
reveal_type(User().role)
# note: Revealed type is 'Role'
```

This will make sure that `team_id` and `role_id` can be accessed. Also, `team` and `role`
will be typed to their right objects.

To be able to access the related manager `Team` and `Role` you could do:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # This doesn't really exists on django so it always need to be imported this way
    from django.db.models.manager import RelatedManager
    from user.models import User


class Team(models.Model):
    if TYPE_CHECKING:
        user_set = RelatedManager["User"]()


class Role(models.Model):
    if TYPE_CHECKING:
        users = RelatedManager["User"]()

reveal_type(Team().user_set)
# note: Revealed type is 'RelatedManager[User]'
reveal_type(Role().users)
# note: Revealed type is 'RelatedManager[User]'
```


### `id Field`

By default Django will create an `AutoField` for you if one doesn't exist.

For type checkers to know about the `id` field you'll need to declare the
field explicitly.

```python
# before
class Post(models.Model):
    ...

# after
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    # OR
    id: int
```

### `HttpRequest`'s `user` property

The `HttpRequest`'s `user` property has a type of `Union[AbstractBaseUser, AnonymousUser]`,
but for most of your views you'll probably want either an authed user or an
`AnonymousUser`.

So we can define a subclass for each case:

```python
class AuthedHttpRequest(HttpRequest):
    user: User  # type: ignore [assignment]
```

And then you can use it in your views:

```python
@auth.login_required
def activity(request: AuthedHttpRequest, team_id: str) -> HttpResponse:
    ...
```

You can also get more strict with your `login_required` decorator so that the
first argument of the fuction it is decorating is `AuthedHttpRequest`:

```python
from typing import Any, Union, TypeVar, cast
from django.http import HttpRequest, HttpResponse
from typing_extensions import Protocol
from functools import wraps

class RequestHandler1(Protocol):
    def __call__(self, request: AuthedHttpRequest) -> HttpResponse:
        ...


class RequestHandler2(Protocol):
    def __call__(self, request: AuthedHttpRequest, __arg1: Any) -> HttpResponse:
        ...


RequestHandler = Union[RequestHandler1, RequestHandler2]


# Verbose bound arg due to limitations of Python typing.
# see: https://github.com/python/mypy/issues/5876
_F = TypeVar("_F", bound=RequestHandler)


def login_required(view_func: _F) -> _F:
    @wraps(view_func)
    def wrapped_view(
        request: AuthedHttpRequest, *args: object, **kwargs: object
    ) -> HttpResponse:
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)  # type: ignore [call-arg]
        raise AuthenticationRequired

    return cast(_F, wrapped_view)
```

Then the following will type error:

```python
@auth.login_required
def activity(request: HttpRequest, team_id: str) -> HttpResponse:
    ...
```

## related

- <https://github.com/sbdchd/djangorestframework-types>
- <https://github.com/sbdchd/celery-types>
- <https://github.com/sbdchd/mongo-types>
- <https://github.com/sbdchd/msgpack-types>
