from __future__ import annotations

from django.contrib.auth.models import User
from django.db.models.deletion import Collector

collector = Collector(using="default")
user = User()
users: tuple[User, ...] = (user,)

collector.collect([user])
collector.collect((user,))
collector.collect(users)
collector.collect(User.objects.all())

# failure cases
collector.collect({user})  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
