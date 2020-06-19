from mypy.types import AnyType, Instance
from mypy.types import Type as MypyType
from mypy.types import TypeOfAny

from mypy_django_plugin.lib import chk_helpers, fullnames, helpers


class QuerySetFilterTypecheckCallback(helpers.GetMethodCallback):
    def resolve_combinable_type(self, combinable_type: Instance) -> MypyType:
        if combinable_type.type.fullname != fullnames.F_EXPRESSION_FULLNAME:
            # Combinables aside from F expressions are unsupported
            return AnyType(TypeOfAny.explicit)

        return self.django_context.resolve_f_expression_type(combinable_type)

    def get_method_return_type(self) -> MypyType:
        lookup_kwargs = self.ctx.arg_names[1]
        provided_lookup_types = self.ctx.arg_types[1]

        if not self.callee_type.args or not isinstance(self.callee_type.args[0], Instance):
            return self.default_return_type

        model_cls_fullname = self.callee_type.args[0].type.fullname
        model_cls = self.django_context.get_model_class_by_fullname(model_cls_fullname)
        if model_cls is None:
            return self.default_return_type

        for lookup_kwarg, provided_type in zip(lookup_kwargs, provided_lookup_types):
            if lookup_kwarg is None:
                continue
            if (isinstance(provided_type, Instance)
                    and provided_type.type.has_base('django.db.models.expressions.Combinable')):
                provided_type = self.resolve_combinable_type(provided_type)

            lookup_type = self.django_context.resolve_lookup_expected_type(self.ctx, model_cls, lookup_kwarg)
            # Managers as provided_type is not supported yet
            if (isinstance(provided_type, Instance)
                    and helpers.has_any_of_bases(provided_type.type, (fullnames.MANAGER_CLASS_FULLNAME,
                                                                      fullnames.QUERYSET_CLASS_FULLNAME))):
                return self.default_return_type

            chk_helpers.check_types_compatible(self.ctx,
                                               expected_type=lookup_type,
                                               actual_type=provided_type,
                                               error_message=f'Incompatible type for lookup {lookup_kwarg!r}:')

        return self.default_return_type
