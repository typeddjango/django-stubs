from __future__ import annotations

from typing import Final

ABSTRACT_BASE_USER_MODEL_FULLNAME: Final = "django.contrib.auth.base_user.AbstractBaseUser"
ABSTRACT_USER_MODEL_FULLNAME: Final = "django.contrib.auth.models.AbstractUser"
PERMISSION_MIXIN_CLASS_FULLNAME: Final = "django.contrib.auth.models.PermissionsMixin"
APPS_FULLNAME: Final = "django.apps.registry.Apps"
STATE_APPS_FULLNAME: Final = "django.db.migrations.state.StateApps"
MODEL_METACLASS_FULLNAME: Final = "django.db.models.base.ModelBase"
MODEL_CLASS_FULLNAME: Final = "django.db.models.base.Model"
FIELD_FULLNAME: Final = "django.db.models.fields.Field"
ARRAY_FIELD_FULLNAME: Final = "django.contrib.postgres.fields.array.ArrayField"
FOREIGN_OBJECT_FULLNAME: Final = "django.db.models.fields.related.ForeignObject"
FOREIGN_KEY_FULLNAME: Final = "django.db.models.fields.related.ForeignKey"
ONETOONE_FIELD_FULLNAME: Final = "django.db.models.fields.related.OneToOneField"
MANYTOMANY_FIELD_FULLNAME: Final = "django.db.models.fields.related.ManyToManyField"
DUMMY_SETTINGS_BASE_CLASS: Final = "django.conf._DjangoConfLazyObject"
AUTH_USER_MODEL_FULLNAME: Final = "django.conf.settings.AUTH_USER_MODEL"

QUERYSET_CLASS_FULLNAME: Final = "django.db.models.query.QuerySet"
BASE_MANAGER_CLASS_FULLNAME: Final = "django.db.models.manager.BaseManager"
MANAGER_CLASS_FULLNAME: Final = "django.db.models.manager.Manager"
RELATED_MANAGER_CLASS: Final = "django.db.models.fields.related_descriptors.RelatedManager"
PREFETCH_CLASS_FULLNAME: Final = "django.db.models.query.Prefetch"
GENERIC_PREFETCH_CLASS_FULLNAME: Final = "django.contrib.contenttypes.prefetch.GenericPrefetch"

CHOICES_CLASS_FULLNAME: Final = "django.db.models.enums.Choices"
CHOICES_TYPE_METACLASS_FULLNAME: Final = "django.db.models.enums.ChoicesType"

WITH_ANNOTATIONS_FULLNAME: Final = "django_stubs_ext.annotations.WithAnnotations"
ANNOTATIONS_FULLNAME: Final = "django_stubs_ext.annotations.Annotations"

ANNOTATED_TYPES_FULLNAMES: Final = {
    "typing.Annotated",
    "typing_extensions.Annotated",
    WITH_ANNOTATIONS_FULLNAME,
}


BASEFORM_CLASS_FULLNAME: Final = "django.forms.forms.BaseForm"
FORM_CLASS_FULLNAME: Final = "django.forms.forms.Form"
MODELFORM_CLASS_FULLNAME: Final = "django.forms.models.ModelForm"

FORM_MIXIN_CLASS_FULLNAME: Final = "django.views.generic.edit.FormMixin"

REVERSE_ONE_TO_ONE_DESCRIPTOR: Final = "django.db.models.fields.related_descriptors.ReverseOneToOneDescriptor"
REVERSE_MANY_TO_ONE_DESCRIPTOR: Final = "django.db.models.fields.related_descriptors.ReverseManyToOneDescriptor"
MANY_TO_MANY_DESCRIPTOR: Final = "django.db.models.fields.related_descriptors.ManyToManyDescriptor"
MANY_RELATED_MANAGER: Final = "django.db.models.fields.related_descriptors.ManyRelatedManager"
RELATED_FIELDS_CLASSES: Final = frozenset(
    (
        FOREIGN_OBJECT_FULLNAME,
        FOREIGN_KEY_FULLNAME,
        ONETOONE_FIELD_FULLNAME,
    )
)

OPTIONS_CLASS_FULLNAME: Final = "django.db.models.options.Options"
QUERYDICT_CLASS_FULLNAME: Final = "django.http.request.QueryDict"

COMBINABLE_EXPRESSION_FULLNAME: Final = "django.db.models.expressions.Combinable"
F_EXPRESSION_FULLNAME: Final = "django.db.models.expressions.F"
FUNC_EXPRESSION_FULLNAME: Final = "django.db.models.expressions.Func"
AGGREGATE_CLASS_FULLNAME: Final = "django.db.models.aggregates.Aggregate"

ANY_ATTR_ALLOWED_CLASS_FULLNAME: Final = "django_stubs_ext.AnyAttrAllowed"
TYPED_MODEL_META_FULLNAME: Final = "django_stubs_ext.db.models.TypedModelMeta"
STR_PROMISE_FULLNAME: Final = "django.utils.functional._StrPromise"

OBJECT_DOES_NOT_EXIST: Final = "django.core.exceptions.ObjectDoesNotExist"
OBJECT_NOT_UPDATED: Final = "django.core.exceptions.ObjectNotUpdated"
MULTIPLE_OBJECTS_RETURNED: Final = "django.core.exceptions.MultipleObjectsReturned"

DJANGO_ABSTRACT_MODELS: Final = frozenset(
    (
        ABSTRACT_BASE_USER_MODEL_FULLNAME,
        ABSTRACT_USER_MODEL_FULLNAME,
        PERMISSION_MIXIN_CLASS_FULLNAME,
        "django.contrib.sessions.base_session.AbstractBaseSession",
    )
)
