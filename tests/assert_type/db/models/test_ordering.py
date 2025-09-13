from django.contrib.auth.models import User
from django.db.models import F, OrderBy
from django.db.models.sql.query import Query

qs = User.objects.all()
qs.order_by("username")
qs.order_by(F("username"))
qs.order_by("-date_joined", F("last_login").desc())

# Test OrderBy expressions (success cases)
qs.order_by(OrderBy(F("username")))
qs.order_by(OrderBy(F("date_joined"), descending=True))
qs.order_by("username", OrderBy(F("last_login"), descending=True))

qs.extra(order_by=["username"])
qs.extra(order_by=[F("username")])
qs.extra(order_by=["username", F("date_joined").desc()])
qs.extra(order_by=[OrderBy(F("username"))])
qs.extra(order_by=["username", OrderBy(F("date_joined"), descending=True)])

query = Query(User)
query.add_ordering("username")
query.add_ordering(F("date_joined"))
query.add_ordering("-last_login", F("username").desc())
query.add_ordering(OrderBy(F("username")))
query.add_ordering("username", OrderBy(F("date_joined"), descending=True))

query.add_extra(
    select=None,
    select_params=None,
    where=None,
    params=None,
    tables=None,
    order_by=["username", F("date_joined").desc(), OrderBy(F("last_login"))],
)

# failure cases
qs.order_by(123)  # type: ignore[arg-type] # pyright: ignore[reportArgumentType]
qs.order_by(["username"])  # type: ignore[arg-type] # pyright: ignore[reportArgumentType]
qs.order_by({"username": "asc"})  # type: ignore[arg-type] # pyright: ignore[reportArgumentType]

qs.extra(order_by=[123])  # type: ignore[list-item] # pyright: ignore[reportArgumentType]
qs.extra(order_by=["username", 456])  # type: ignore[list-item] # pyright: ignore[reportArgumentType]

query.add_ordering(123)  # type: ignore[arg-type] # pyright: ignore[reportArgumentType]
query.add_ordering(["username"])  # type: ignore[arg-type] # pyright: ignore[reportArgumentType]

query.add_extra(
    select=None,
    select_params=None,
    where=None,
    params=None,
    tables=None,
    order_by=[123, "username"],  # type: ignore[list-item] # pyright: ignore[reportArgumentType]
)
