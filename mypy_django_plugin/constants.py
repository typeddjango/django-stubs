# Django fields that has to= attribute used to retrieve original model
REFERENCING_DB_FIELDS = {
    'django.db.models.fields.related.ForeignKey',
    'django.db.models.fields.related.OneToOneField'
}

# mapping between field types and plain python types
DB_FIELDS_TO_TYPES = {
    'django.db.models.fields.CharField': 'builtins.str',
    'django.db.models.fields.TextField': 'builtins.str',
    'django.db.models.fields.IntegerField': 'builtins.int',
    'django.db.models.fields.FloatField': 'builtins.float'
}
