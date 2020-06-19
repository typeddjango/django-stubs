from typing import Optional

from mypy.types import Type as MypyType, Instance, TypeType, CallableType, NoneTyp

from mypy_django_plugin.lib import sem_helpers, helpers, chk_helpers


class FormCallback(helpers.ClassDefPluginCallback):
    def modify_class_defn(self) -> None:
        meta_node = sem_helpers.get_nested_meta_node_for_current_class(self.class_defn.info)
        if meta_node is None:
            return None
        meta_node.fallback_to_any = True


class FormMethodCallback(helpers.GetMethodCallback):
    def get_specified_form_class(self, object_type: Instance) -> Optional[TypeType]:
        form_class_sym = object_type.type.get('form_class')
        if form_class_sym and isinstance(form_class_sym.type, CallableType):
            return TypeType(form_class_sym.type.ret_type)
        return None


class GetFormCallback(FormMethodCallback):
    def get_method_return_type(self) -> MypyType:
        object_type = self.ctx.type
        assert isinstance(object_type, Instance)

        form_class_type = chk_helpers.get_call_argument_type_by_name(self.ctx, 'form_class')
        if form_class_type is None or isinstance(form_class_type, NoneTyp):
            form_class_type = self.get_specified_form_class(object_type)

        if isinstance(form_class_type, TypeType) and isinstance(form_class_type.item, Instance):
            return form_class_type.item

        if isinstance(form_class_type, CallableType) and isinstance(form_class_type.ret_type, Instance):
            return form_class_type.ret_type

        return self.default_return_type


class GetFormClassCallback(FormMethodCallback):
    def get_method_return_type(self) -> MypyType:
        object_type = self.ctx.type
        assert isinstance(object_type, Instance)

        form_class_type = self.get_specified_form_class(object_type)
        if form_class_type is None:
            return self.default_return_type

        return form_class_type
