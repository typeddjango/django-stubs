ABSTRACT_USER_MODEL_FULLNAME = "django.contrib.auth.models.AbstractUser"
PERMISSION_MIXIN_CLASS_FULLNAME = "django.contrib.auth.models.PermissionsMixin"
MODEL_METACLASS_FULLNAME = "django.db.models.base.ModelBase"
MODEL_CLASS_FULLNAME = "django.db.models.base.Model"
FIELD_FULLNAME = "django.db.models.fields.Field"
CHAR_FIELD_FULLNAME = "django.db.models.fields.CharField"
ARRAY_FIELD_FULLNAME = "django.contrib.postgres.fields.array.ArrayField"
AUTO_FIELD_FULLNAME = "django.db.models.fields.AutoField"
GENERIC_FOREIGN_KEY_FULLNAME = "django.contrib.contenttypes.fields.GenericForeignKey"
FOREIGN_OBJECT_FULLNAME = "django.db.models.fields.related.ForeignObject"
FOREIGN_KEY_FULLNAME = "django.db.models.fields.related.ForeignKey"
ONETOONE_FIELD_FULLNAME = "django.db.models.fields.related.OneToOneField"
MANYTOMANY_FIELD_FULLNAME = "django.db.models.fields.related.ManyToManyField"
DUMMY_SETTINGS_BASE_CLASS = "django.conf._DjangoConfLazyObject"
AUTH_USER_MODEL_FULLNAME = "django.conf.settings.AUTH_USER_MODEL"

QUERYSET_CLASS_FULLNAME = "django.db.models.query.QuerySet"
BASE_MANAGER_CLASS_FULLNAME = "django.db.models.manager.BaseManager"
MANAGER_CLASS_FULLNAME = "django.db.models.manager.Manager"
RELATED_MANAGER_CLASS = "django.db.models.fields.related_descriptors.RelatedManager"

WITH_ANNOTATIONS_FULLNAME = "django_stubs_ext.WithAnnotations"
ANNOTATIONS_FULLNAME = "django_stubs_ext.annotations.Annotations"

BASEFORM_CLASS_FULLNAME = "django.forms.forms.BaseForm"
FORM_CLASS_FULLNAME = "django.forms.forms.Form"
MODELFORM_CLASS_FULLNAME = "django.forms.models.ModelForm"

FORM_MIXIN_CLASS_FULLNAME = "django.views.generic.edit.FormMixin"

MANAGER_CLASSES = {
    MANAGER_CLASS_FULLNAME,
    BASE_MANAGER_CLASS_FULLNAME,
}

REVERSE_ONE_TO_ONE_DESCRIPTOR = "django.db.models.fields.related_descriptors.ReverseOneToOneDescriptor"
MANY_TO_MANY_DESCRIPTOR = "django.db.models.fields.related_descriptors.ManyToManyDescriptor"
MANY_RELATED_MANAGER = "django.db.models.fields.related_descriptors.ManyRelatedManager"
RELATED_FIELDS_CLASSES = frozenset(
    (
        FOREIGN_OBJECT_FULLNAME,
        FOREIGN_KEY_FULLNAME,
        ONETOONE_FIELD_FULLNAME,
    )
)

MIGRATION_CLASS_FULLNAME = "django.db.migrations.migration.Migration"
OPTIONS_CLASS_FULLNAME = "django.db.models.options.Options"
HTTPREQUEST_CLASS_FULLNAME = "django.http.request.HttpRequest"
QUERYDICT_CLASS_FULLNAME = "django.http.request.QueryDict"

COMBINABLE_EXPRESSION_FULLNAME = "django.db.models.expressions.Combinable"
F_EXPRESSION_FULLNAME = "django.db.models.expressions.F"

ANY_ATTR_ALLOWED_CLASS_FULLNAME = "django_stubs_ext.AnyAttrAllowed"

STR_PROMISE_FULLNAME = "django.utils.functional._StrPromise"

OBJECT_DOES_NOT_EXIST = "django.core.exceptions.ObjectDoesNotExist"
MULTIPLE_OBJECTS_RETURNED = "django.core.exceptions.MultipleObjectsReturned"

DJANGO_ABSTRACT_MODELS = frozenset(
    (
        "django.contrib.auth.base_user.AbstractBaseUser",
        ABSTRACT_USER_MODEL_FULLNAME,
        PERMISSION_MIXIN_CLASS_FULLNAME,
        "django.contrib.sessions.base_session.AbstractBaseSession",
    )
)
