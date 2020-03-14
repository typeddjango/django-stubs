from mypy.checker import gen_unique_name
from mypy.plugin import AttributeContext
from mypy.types import Instance
from mypy.types import Type as MypyType

from django.db.models.fields.reverse_related import ForeignObjectRel, OneToOneRel, ManyToOneRel, ManyToManyRel

from mypy_django_plugin.lib import helpers, fullnames
from mypy_django_plugin.lib.helpers import GetAttributeCallback


class GetRelatedManagerCallback(GetAttributeCallback):
    obj_type: Instance

    def get_related_manager_type(self, relation: ForeignObjectRel) -> MypyType:
        related_model_cls = self.django_context.get_field_related_model_cls(relation)
        if related_model_cls is None:
            # could not find a referenced model (maybe invalid to= value, or GenericForeignKey)
            # TODO: show error
            return self.default_attr_type

        related_model_info = self.lookup_typeinfo(helpers.get_class_fullname(related_model_cls))
        if related_model_info is None:
            # TODO: show error
            return self.default_attr_type

        if isinstance(relation, OneToOneRel):
            return Instance(related_model_info, [])

        elif isinstance(relation, (ManyToOneRel, ManyToManyRel)):
            related_manager_info = self.lookup_typeinfo(fullnames.RELATED_MANAGER_CLASS)
            if related_manager_info is None:
                return self.default_attr_type

            # get type of default_manager for model
            default_manager_fullname = helpers.get_class_fullname(related_model_cls._meta.default_manager.__class__)
            default_manager_info = self.lookup_typeinfo(default_manager_fullname)
            if default_manager_info is None:
                return self.default_attr_type

            default_manager_type = Instance(default_manager_info, [Instance(related_model_info, [])])
            related_manager_type = Instance(related_manager_info,
                                            [Instance(related_model_info, [])])

            if (not isinstance(default_manager_type, Instance)
                    or default_manager_type.type.fullname == fullnames.MANAGER_CLASS_FULLNAME):
                # if not defined or trivial -> just return RelatedManager[Model]
                return related_manager_type

            # make anonymous class
            name = gen_unique_name(related_model_cls.__name__ + '_' + 'RelatedManager',
                                   self.obj_type.type.names)
            bases = [related_manager_type, default_manager_type]
            new_manager_info = self.new_typeinfo(name, bases)
            return Instance(new_manager_info, [])

    def __call__(self, ctx: AttributeContext):
        super().__call__(ctx)
        assert isinstance(self.obj_type, Instance)

        model_fullname = self.obj_type.type.fullname
        model_cls = self.django_context.get_model_class_by_fullname(model_fullname)
        if model_cls is None:
            return self.default_attr_type
        for reverse_manager_name, relation in self.django_context.get_model_relations(model_cls):
            if reverse_manager_name == self.name:
                return self.get_related_manager_type(relation)

        return self.default_attr_type
