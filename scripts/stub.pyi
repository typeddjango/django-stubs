DJANGO_2_2 = 1
DJANGO_3_0 = 2

class MyClass:
    if DJANGO_3_0:
        def django_3_0_func(self, a: int) -> int: ...
    else:
        def django_2_2_func(self, a: str) -> str: ...

    if DJANGO_3_0:
        def only_django_3_0_func(self, a: int) -> int: ...
