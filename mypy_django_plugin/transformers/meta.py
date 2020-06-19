from django.core.exceptions import FieldDoesNotExist
from mypy.types import AnyType, Instance
from mypy.types import Type as MypyType
from mypy.types import TypeOfAny

from mypy_django_plugin.lib import chk_helpers, helpers


class MetaGetFieldCallback(helpers.GetMethodCallback):
    def _get_field_instance(self, field_fullname: str) -> MypyType:
        field_info = helpers.lookup_fully_qualified_typeinfo(self.type_checker, field_fullname)
        if field_info is None:
            return AnyType(TypeOfAny.unannotated)
        return Instance(field_info, [AnyType(TypeOfAny.explicit), AnyType(TypeOfAny.explicit)])

    def get_method_return_type(self) -> MypyType:
        # bail if list of generic params is empty
        if len(self.callee_type.args) == 0:
            return self.default_return_type

        model_type = self.callee_type.args[0]
        if not isinstance(model_type, Instance):
            return self.default_return_type

        model_cls = self.django_context.get_model_class_by_fullname(model_type.type.fullname)
        if model_cls is None:
            return self.default_return_type

        field_name_expr = chk_helpers.get_call_argument_by_name(self.ctx, 'field_name')
        if field_name_expr is None:
            return self.default_return_type

        field_name = helpers.resolve_string_attribute_value(field_name_expr, self.django_context)
        if field_name is None:
            return self.default_return_type

        try:
            field = model_cls._meta.get_field(field_name)
        except FieldDoesNotExist as exc:
            # if model is abstract, do not raise exception, skip false positives
            if not model_cls._meta.abstract:
                self.ctx.api.fail(exc.args[0], self.ctx.context)
            return AnyType(TypeOfAny.from_error)

        field_fullname = helpers.get_class_fullname(field.__class__)
        return self._get_field_instance(field_fullname)
