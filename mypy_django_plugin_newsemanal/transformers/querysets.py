from mypy.plugin import AnalyzeTypeContext, FunctionContext
from mypy.types import AnyType, Instance, Type as MypyType, TypeOfAny

from mypy_django_plugin_newsemanal.lib import fullnames, helpers


def set_first_generic_param_as_default_for_second(ctx: AnalyzeTypeContext, fullname: str) -> MypyType:
    if not ctx.type.args:
        try:
            return ctx.api.named_type(fullname, [AnyType(TypeOfAny.explicit),
                                                 AnyType(TypeOfAny.explicit)])
        except KeyError:
            # really should never happen
            return AnyType(TypeOfAny.explicit)

    args = ctx.type.args
    if len(args) == 1:
        args = [args[0], args[0]]

    analyzed_args = [ctx.api.analyze_type(arg) for arg in args]
    ctx.api.analyze_type(ctx.type)
    try:
        return ctx.api.named_type(fullname, analyzed_args)
    except KeyError:
        return AnyType(TypeOfAny.explicit)


def determine_proper_manager_type(ctx: FunctionContext) -> MypyType:
    ret = ctx.default_return_type
    assert isinstance(ret, Instance)

    if not ctx.api.tscope.classes:
        # not in class
        return ret
    outer_model_info = ctx.api.tscope.classes[0]
    if not outer_model_info.has_base(fullnames.MODEL_CLASS_FULLNAME):
        return ret

    return helpers.reparametrize_instance(ret, [Instance(outer_model_info, [])])
