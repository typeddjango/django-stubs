import dataclasses
from mypy import types, nodes
from mypy.nodes import CallExpr, StrExpr, AssignmentStmt, RefExpr
from mypy.plugin import AttributeContext, ClassDefContext, SemanticAnalyzerPluginInterface
from mypy.types import Type, Instance, AnyType, TypeOfAny

from mypy_django_plugin.helpers import lookup_django_model, get_app_model
from mypy_django_plugin.model_classes import DjangoModelsRegistry

# mapping between field types and plain python types
DB_FIELDS_TO_TYPES = {
    'django.db.models.fields.CharField': 'builtins.str',
    'django.db.models.fields.TextField': 'builtins.str',
    'django.db.models.fields.BooleanField': 'builtins.bool',
    # 'django.db.models.fields.NullBooleanField': 'typing.Optional[builtins.bool]',
    'django.db.models.fields.IntegerField': 'builtins.int',
    'django.db.models.fields.AutoField': 'builtins.int',
    'django.db.models.fields.FloatField': 'builtins.float',
    'django.contrib.postgres.fields.jsonb.JSONField': 'builtins.dict',
    'django.contrib.postgres.fields.array.ArrayField': 'typing.Iterable'
}


# def get_queryset_of(type_fullname: str):
#     return model_definition.api.lookup_fully_qualified_or_none('django.db.models.QuerySet')


@dataclasses.dataclass
class DjangoPluginApi(object):
    mypy_api: SemanticAnalyzerPluginInterface

    def get_queryset_of(self, type_fullname: str = 'django.db.models.base.Model') -> types.Type:
        queryset_sym = self.mypy_api.lookup_fully_qualified_or_none('django.db.models.QuerySet')
        if not queryset_sym:
            return AnyType(TypeOfAny.from_error)

        generic_arg = self.mypy_api.lookup_fully_qualified_or_none(type_fullname)
        if not generic_arg:
            return Instance(queryset_sym.node, [AnyType(TypeOfAny.from_error)])

        return Instance(queryset_sym.node, [Instance(generic_arg.node, [])])

    def generate_related_manager_assignment_stmt(self,
                                                 related_mngr_name: str,
                                                 queryset_argument_type_fullname: str) -> nodes.AssignmentStmt:
        rvalue = nodes.TempNode(AnyType(TypeOfAny.special_form))
        assignment = nodes.AssignmentStmt(lvalues=[nodes.NameExpr(related_mngr_name)],
                                          rvalue=rvalue,
                                          new_syntax=True,
                                          type=self.get_queryset_of(queryset_argument_type_fullname))
        return assignment


class DetermineFieldPythonTypeCallback(object):
    def __init__(self, models_registry: DjangoModelsRegistry):
        self.models_registry = models_registry

    def __call__(self, attr_context: AttributeContext) -> Type:
        default_attr_type = attr_context.default_attr_type

        if isinstance(default_attr_type, Instance):
            attr_type_fullname = default_attr_type.type.fullname()
            if attr_type_fullname in DB_FIELDS_TO_TYPES:
                return attr_context.api.named_type(DB_FIELDS_TO_TYPES[attr_type_fullname])

            # if 'base' in default_attr_type.type.metadata:
            #     referred_base_model = default_attr_type.type.metadata['base']

            if 'members' in attr_context.type.type.metadata:
                arg_name = attr_context.context.name
                if arg_name in attr_context.type.type.metadata['members']:
                    referred_base_model = attr_context.type.type.metadata['members'][arg_name]

                    typ = lookup_django_model(attr_context.api, referred_base_model)
                    try:
                        return Instance(typ.node, [])
                    except AssertionError as e:
                        return typ.type

        return default_attr_type


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


class CollectModelsInformationCallback(object):
    def __init__(self, model_registry: DjangoModelsRegistry):
        self.model_registry = model_registry

    def __call__(self, model_definition: ClassDefContext) -> None:
        self.model_registry.base_models.add(model_definition.cls.fullname)
        plugin_api = DjangoPluginApi(mypy_api=model_definition.api)

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

                            referred_to_model = rvalue.args[rvalue.arg_names.index('to')]
                            if isinstance(referred_to_model, StrExpr):
                                referred_model_fullname = get_app_model(referred_to_model.value)
                            else:
                                referred_model_fullname = referred_to_model.fullname

                            rvalue.callee.node.metadata['base'] = referred_model_fullname

                            referred_model = model_definition.api.lookup_fully_qualified_or_none(referred_model_fullname)

                            if 'related_name' in rvalue.arg_names:
                                related_arg_value = rvalue.args[rvalue.arg_names.index('related_name')].value
                                referred_model_class_def = referred_model.node.defn  # type: nodes.ClassDef

                                referred_model_class_def.defs.body.append(
                                    plugin_api.generate_related_manager_assignment_stmt(related_arg_value,
                                                                                        model_definition.cls.fullname))

                        if rvalue.callee.fullname == 'django.db.models.fields.related.OneToOneField':
                            referred_to_model = rvalue.args[rvalue.arg_names.index('to')]
                            if isinstance(referred_to_model, StrExpr):
                                referred_model_fullname = get_app_model(referred_to_model.value)
                            else:
                                referred_model_fullname = referred_to_model.fullname

                            referred_model = model_definition.api.lookup_fully_qualified_or_none(referred_model_fullname)

                            if 'related_name' in rvalue.arg_names:
                                related_arg_value = rvalue.args[rvalue.arg_names.index('related_name')].value
                                referred_model.node.names[related_arg_value] = \
                                    model_definition.api.lookup_fully_qualified_or_none(model_definition.cls.fullname)

                            rvalue.callee.node.metadata['base'] = referred_model_fullname

                        rvalue.callee.node.metadata['name'] = arg_name
                        if 'members' not in model_definition.cls.info.metadata:
                            model_definition.cls.info.metadata['members'] = {}

                        model_definition.cls.info.metadata['members'][arg_name] = rvalue.callee.node.metadata.get('base', None)
