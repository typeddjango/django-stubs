from typing import Optional, Tuple, cast

from django.db.models.fields import Field
from django.db.models.fields.related import RelatedField
from mypy.checkexpr import FunctionContext
from mypy.nodes import AssignmentStmt, NameExpr, TypeInfo
from mypy.types import AnyType, Instance
from mypy.types import Type as MypyType
from mypy.types import TypeOfAny

from mypy_django_plugin.lib import chk_helpers, fullnames, helpers


def reparametrize_related_field_type(related_field_type: Instance,
                                     set_type: MypyType,
                                     get_type: MypyType
                                     ) -> Instance:
    args = [
        helpers.convert_any_to_type(related_field_type.args[0], set_type),
        helpers.convert_any_to_type(related_field_type.args[1], get_type),
    ]
    return helpers.reparametrize_instance(related_field_type, new_args=args)


def get_field_descriptor_types(field_info: TypeInfo, is_nullable: bool) -> Tuple[MypyType, MypyType]:
    set_type = helpers.get_private_descriptor_type(field_info, '_pyi_private_set_type',
                                                   is_nullable=is_nullable)
    get_type = helpers.get_private_descriptor_type(field_info, '_pyi_private_get_type',
                                                   is_nullable=is_nullable)
    return set_type, get_type


def get_field_type(field_info: TypeInfo, is_nullable: bool) -> Instance:
    set_type, get_type = get_field_descriptor_types(field_info, is_nullable)
    return Instance(field_info, [set_type, get_type])


def set_descriptor_types_for_field(ctx: FunctionContext) -> Instance:
    default_return_type = cast(Instance, ctx.default_return_type)

    is_nullable = False
    null_expr = chk_helpers.get_call_argument_by_name(ctx, 'null')
    if null_expr is not None:
        is_nullable = helpers.parse_bool(null_expr) or False

    set_type, get_type = get_field_descriptor_types(default_return_type.type, is_nullable)
    return helpers.reparametrize_instance(default_return_type, [set_type, get_type])


class FieldContructorCallback(helpers.GetFunctionCallback):
    default_return_type: Instance

    def _get_field_from_model_cls_assignment(self) -> Optional[Field]:
        """ Use AssignmentStmt inside model class declaration to find instance of Field (from DjangoContext)"""
        outer_model_info = self.type_checker.scope.active_class()
        if (outer_model_info is None
                or not self.django_context.is_model_subclass(outer_model_info)):
            return None

        field_name = None
        for stmt in outer_model_info.defn.defs.body:
            if isinstance(stmt, AssignmentStmt):
                if stmt.rvalue == self.ctx.context:
                    if not isinstance(stmt.lvalues[0], NameExpr):
                        return None
                    field_name = stmt.lvalues[0].name
                    break
        if field_name is None:
            return None

        model_cls = self.django_context.get_model_class_by_fullname(outer_model_info.fullname)
        if model_cls is None:
            return None

        current_field = model_cls._meta.get_field(field_name)
        return current_field

    def current_field_type(self) -> Instance:
        is_nullable = False
        null_expr = chk_helpers.get_call_argument_by_name(self.ctx, 'null')
        if null_expr is not None:
            is_nullable = helpers.parse_bool(null_expr) or False

        set_type, get_type = get_field_descriptor_types(self.default_return_type.type, is_nullable)
        return helpers.reparametrize_instance(self.default_return_type, [set_type, get_type])

    def array_field_type(self) -> MypyType:
        default_array_field_type = self.current_field_type()

        base_field_arg_type = chk_helpers.get_call_argument_type_by_name(self.ctx, 'base_field')
        if not base_field_arg_type or not isinstance(base_field_arg_type, Instance):
            return default_array_field_type

        base_type = base_field_arg_type.args[1]  # extract __get__ type
        args = []
        for default_arg in default_array_field_type.args:
            args.append(helpers.convert_any_to_type(default_arg, base_type))

        return helpers.reparametrize_instance(default_array_field_type, args)

    def related_field_type(self) -> MypyType:
        current_field = self._get_field_from_model_cls_assignment()
        if current_field is None:
            return AnyType(TypeOfAny.from_error)

        assert isinstance(current_field, RelatedField)

        related_model_cls = self.django_context.get_field_related_model_cls(current_field)
        if related_model_cls is None:
            return AnyType(TypeOfAny.from_error)

        default_related_field_type = set_descriptor_types_for_field(self.ctx)

        # self reference with abstract=True on the model where ForeignKey is defined
        current_model_cls = current_field.model
        if (current_model_cls._meta.abstract
                and current_model_cls == related_model_cls):
            # for all derived non-abstract classes, set variable with this name to
            # __get__/__set__ of ForeignKey of derived model
            for model_cls in self.django_context.all_registered_model_classes:
                if issubclass(model_cls, current_model_cls) and not model_cls._meta.abstract:
                    derived_model_info = helpers.lookup_class_typeinfo(self.type_checker, model_cls)
                    if derived_model_info is not None:
                        fk_ref_type = Instance(derived_model_info, [])
                        derived_fk_type = reparametrize_related_field_type(default_related_field_type,
                                                                           set_type=fk_ref_type, get_type=fk_ref_type)
                        chk_helpers.add_new_sym_for_info(derived_model_info,
                                                         name=current_field.name,
                                                         sym_type=derived_fk_type)

        related_model = related_model_cls
        related_model_to_set = related_model_cls
        if related_model_to_set._meta.proxy_for_model is not None:
            related_model_to_set = related_model_to_set._meta.proxy_for_model

        related_model_info = helpers.lookup_class_typeinfo(self.type_checker, related_model)
        if related_model_info is None:
            # maybe no type stub
            related_model_type = AnyType(TypeOfAny.unannotated)
        else:
            related_model_type = Instance(related_model_info, [])  # type: ignore

        related_model_to_set_info = helpers.lookup_class_typeinfo(self.type_checker, related_model_to_set)
        if related_model_to_set_info is None:
            # maybe no type stub
            related_model_to_set_type = AnyType(TypeOfAny.unannotated)
        else:
            related_model_to_set_type = Instance(related_model_to_set_info, [])  # type: ignore

        # replace Any with referred_to_type
        return reparametrize_related_field_type(default_related_field_type,
                                                set_type=related_model_to_set_type,
                                                get_type=related_model_type)

    def get_function_return_type(self) -> MypyType:
        outer_model_info = self.type_checker.scope.active_class()
        if (outer_model_info is None
                or not self.django_context.is_model_subclass(outer_model_info)):
            return self.default_return_type

        assert isinstance(outer_model_info, TypeInfo)

        if helpers.has_any_of_bases(self.default_return_type.type, fullnames.RELATED_FIELDS_CLASSES):
            return self.related_field_type()

        if self.default_return_type.type.has_base(fullnames.ARRAY_FIELD_FULLNAME):
            return self.array_field_type()

        return self.current_field_type()
