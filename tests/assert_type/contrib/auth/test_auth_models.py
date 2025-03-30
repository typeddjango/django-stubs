from datetime import datetime
from typing import Optional

from django.contrib.auth.models import Group, Group_permissions, Permission, User, User_groups, User_permissions
from django.contrib.contenttypes.models import ContentType
from django.db.models import Manager
from typing_extensions import assert_type

user = User()
assert_type(user.id, int)
assert_type(user.pk, int)
assert_type(user.password, str)
assert_type(user.last_login, Optional[datetime])
assert_type(user.is_active, bool)
assert_type(user.username, str)
assert_type(user.first_name, str)
assert_type(user.last_name, str)
assert_type(user.email, str)
assert_type(user.is_staff, bool)
assert_type(user.is_active, bool)
assert_type(user.date_joined, datetime)
assert_type(user.groups.get(), Group)
assert_type(user.groups.through, type[User_groups])
assert_type(user.user_permissions.get(), Permission)
assert_type(user.user_permissions.through, type[User_permissions])

group = Group()
assert_type(group.id, int)
assert_type(group.pk, int)
assert_type(group.name, str)
assert_type(group.permissions.get(), Permission)
assert_type(group.permissions.through, type[Group_permissions])
assert_type(Group.permissions.through, type[Group_permissions])
assert_type(Group.permissions.through.objects, Manager[Group_permissions])

group_permissions = Group.permissions.through.objects.get()
assert_type(group_permissions.id, int)
assert_type(group_permissions.pk, int)
assert_type(group_permissions.group, Group)
assert_type(group_permissions.group_id, int)
assert_type(group_permissions.permission, Permission)
assert_type(group_permissions.permission_id, int)

permission = Permission()
assert_type(permission.id, int)
assert_type(permission.pk, int)
assert_type(permission.name, str)
assert_type(permission.content_type, ContentType)
assert_type(permission.content_type_id, int)
assert_type(permission.group_set.get(), Group)
assert_type(permission.group_set.through.objects.get(), Group_permissions)
