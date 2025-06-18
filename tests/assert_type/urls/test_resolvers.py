from django.urls.resolvers import ResolverMatch


def f(x: ResolverMatch) -> None:
    _func, _args, _kwargs = x  # does not error
    # would be nice but we can't really get this without tuple specialization
    # as `__getitem__` is implemented as `return (..., ...)[...]`
    # assert_type(_func, Callable)
