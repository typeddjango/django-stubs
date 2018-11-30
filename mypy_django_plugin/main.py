import os
from typing import Callable, Optional, cast

from mypy.nodes import AssignmentStmt, CallExpr, MemberExpr, StrExpr, NameExpr
from mypy.options import Options
from mypy.plugin import Plugin, FunctionContext, ClassDefContext
from mypy.semanal import SemanticAnalyzerPass2
from mypy.types import Type, Instance

from mypy_django_plugin import helpers, monkeypatch
from mypy_django_plugin.plugins.meta_inner_class import inject_any_as_base_for_nested_class_meta
from mypy_django_plugin.plugins.objects_queryset import set_objects_queryset_to_model_class
from mypy_django_plugin.plugins.fields import determine_type_of_array_field, \
    add_int_id_attribute_if_primary_key_true_is_not_present
from mypy_django_plugin.plugins.related_fields import set_fieldname_attrs_for_related_fields, add_new_var_node_to_class, \
    extract_to_parameter_as_get_ret_type
from mypy_django_plugin.plugins.setup_settings import DjangoConfSettingsInitializerHook


base_model_classes = {helpers.MODEL_CLASS_FULLNAME}


def add_related_managers_from_referred_foreign_keys_to_model(ctx: ClassDefContext) -> None:
    api = cast(SemanticAnalyzerPass2, ctx.api)
    for stmt in ctx.cls.defs.body:
        if not isinstance(stmt, AssignmentStmt):
            continue
        if len(stmt.lvalues) > 1:
            # not supported yet
            continue
        rvalue = stmt.rvalue
        if not isinstance(rvalue, CallExpr):
            continue
        if (not isinstance(rvalue.callee, MemberExpr)
                or not rvalue.callee.fullname in {helpers.FOREIGN_KEY_FULLNAME,
                                                  helpers.ONETOONE_FIELD_FULLNAME}):
            continue
        if 'related_name' not in rvalue.arg_names:
            # positional related_name is not supported yet
            continue
        related_name = rvalue.args[rvalue.arg_names.index('related_name')].value

        if 'to' in rvalue.arg_names:
            expr = rvalue.args[rvalue.arg_names.index('to')]
        else:
            # first positional argument
            expr = rvalue.args[0]

        if isinstance(expr, StrExpr):
            model_typeinfo = helpers.get_model_type_from_string(expr,
                                                                all_modules=api.modules)
            if model_typeinfo is None:
                continue
        elif isinstance(expr, NameExpr):
            model_typeinfo = expr.node
        else:
            continue

        if rvalue.callee.fullname == helpers.FOREIGN_KEY_FULLNAME:
            typ = api.named_type_or_none(helpers.QUERYSET_CLASS_FULLNAME,
                                         args=[Instance(ctx.cls.info, [])])
        else:
            typ = Instance(ctx.cls.info, [])

        if typ is None:
            continue
        add_new_var_node_to_class(model_typeinfo, related_name, typ)


class TransformModelClassHook(object):
    def __call__(self, ctx: ClassDefContext) -> None:
        base_model_classes.add(ctx.cls.fullname)

        set_fieldname_attrs_for_related_fields(ctx)
        set_objects_queryset_to_model_class(ctx)
        inject_any_as_base_for_nested_class_meta(ctx)
        add_related_managers_from_referred_foreign_keys_to_model(ctx)
        add_int_id_attribute_if_primary_key_true_is_not_present(ctx)


class DjangoPlugin(Plugin):
    def __init__(self,
                 options: Options) -> None:
        super().__init__(options)
        monkeypatch.replace_apply_function_plugin_method()
        monkeypatch.make_inner_classes_with_inherit_from_any_compatible_with_each_other()

        self.django_settings = os.environ.get('DJANGO_SETTINGS_MODULE')
        if self.django_settings:
            monkeypatch.load_graph_to_add_settings_file_as_a_source_seed(self.django_settings)
            monkeypatch.inject_dependencies(self.django_settings)
            # monkeypatch.process_settings_before_dependants(self.django_settings)
        else:
            monkeypatch.restore_original_load_graph()
            monkeypatch.restore_original_dependencies_handling()

    def get_function_hook(self, fullname: str
                          ) -> Optional[Callable[[FunctionContext], Type]]:
        if fullname in {helpers.FOREIGN_KEY_FULLNAME,
                        helpers.ONETOONE_FIELD_FULLNAME}:
            return extract_to_parameter_as_get_ret_type

        # if fullname == helpers.ONETOONE_FIELD_FULLNAME:
        #     return OneToOneFieldHook(settings=self.django_settings)

        if fullname == 'django.contrib.postgres.fields.array.ArrayField':
            return determine_type_of_array_field
        return None

    def get_base_class_hook(self, fullname: str
                            ) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname in base_model_classes:
            return TransformModelClassHook()

        if fullname == helpers.DUMMY_SETTINGS_BASE_CLASS:
            return DjangoConfSettingsInitializerHook(settings_module=self.django_settings)

        return None


def plugin(version):
    return DjangoPlugin
