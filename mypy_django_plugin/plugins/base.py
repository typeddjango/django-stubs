from typing import Callable, Optional

from mypy.nodes import AssignmentStmt, CallExpr, RefExpr, StrExpr
from mypy.plugin import Plugin, ClassDefContext

from mypy_django_plugin.helpers import get_app_model
from mypy_django_plugin.model_classes import DjangoModelsRegistry


# fields which real type is inside to= expression
REFERENCING_DB_FIELDS = {
    'django.db.models.fields.related.ForeignKey',
    'django.db.models.fields.related.OneToOneField'
}


def save_referred_to_model_in_metadata(rvalue: CallExpr) -> None:
    to_arg_value = rvalue.args[rvalue.arg_names.index('to')]
    if isinstance(to_arg_value, StrExpr):
        referred_model_fullname = get_app_model(to_arg_value.value)
    else:
        referred_model_fullname = to_arg_value.fullname

    rvalue.callee.node.metadata['base'] = referred_model_fullname


class CollectModelsInformation(object):
    def __init__(self, model_registry: DjangoModelsRegistry):
        self.model_registry = model_registry

    def __call__(self, model_definition: ClassDefContext) -> None:
        self.model_registry.base_models.add(model_definition.cls.fullname)

        for member in model_definition.cls.defs.body:
            if isinstance(member, AssignmentStmt):
                if len(member.lvalues) > 1:
                    return None

                arg_name = member.lvalues[0].name
                arg_name_as_id = arg_name + '_id'

                rvalue = member.rvalue
                if isinstance(rvalue, CallExpr):
                    if not isinstance(rvalue.callee, RefExpr):
                        return None

                    if rvalue.callee.fullname in REFERENCING_DB_FIELDS:
                        if rvalue.callee.fullname == 'django.db.models.fields.related.ForeignKey':
                            model_definition.cls.info.names[arg_name_as_id] = \
                                model_definition.api.lookup_fully_qualified('builtins.int')

                        if rvalue.callee.fullname == 'django.db.models.fields.related.OneToOneField':
                            if 'related_name' in rvalue.arg_names:
                                referred_to_model = rvalue.args[rvalue.arg_names.index('to')]
                                related_arg_value = rvalue.args[rvalue.arg_names.index('related_name')].value

                                if isinstance(referred_to_model, StrExpr):
                                    referred_model_fullname = get_app_model(referred_to_model.value)
                                else:
                                    referred_model_fullname = referred_to_model.fullname

                                referred_model = model_definition.api.lookup_fully_qualified_or_none(referred_model_fullname)
                                referred_model.node.names[related_arg_value] = \
                                    model_definition.api.lookup_fully_qualified_or_none(model_definition.cls.fullname)

                        return save_referred_to_model_in_metadata(rvalue)


class BaseDjangoModelsPlugin(Plugin):
    model_registry = DjangoModelsRegistry()

    def get_base_class_hook(self, fullname: str
                            ) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname in self.model_registry:
            return CollectModelsInformation(self.model_registry)

        return None
