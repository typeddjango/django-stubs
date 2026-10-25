from __future__ import annotations

from typing import assert_type

from django.dispatch import Signal, receiver

signal = Signal()


@receiver([signal, signal], sender=object, dispatch_uid="uid")
def handler(sender: object, **kwargs: object) -> int:
    return 1


assert_type(handler(object()), int)
