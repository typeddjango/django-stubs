from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from typing_extensions import assert_type

content_type = ContentType()
assert_type(content_type.id, int)
assert_type(content_type.pk, int)
assert_type(content_type.app_label, str)
assert_type(content_type.model, str)
assert_type(content_type.logentry_set.get(), LogEntry)
assert_type(content_type.permission_set.get(), Permission)
