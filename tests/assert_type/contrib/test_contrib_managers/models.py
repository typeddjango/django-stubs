from __future__ import annotations

from typing import assert_type

from django.contrib.admin.models import LogEntry, LogEntryManager
from django.contrib.auth.models import Group, GroupManager, Permission, PermissionManager
from django.contrib.sites.models import Site, SiteManager
from django.db.models import QuerySet


class ProxyGroup(Group):
    class Meta:
        proxy = True


class ProxyPermission(Permission):
    class Meta:
        proxy = True


class ProxySite(Site):
    class Meta:
        proxy = True


class ProxyLogEntry(LogEntry):
    class Meta:
        proxy = True


def group_manager_is_bound_to_the_model() -> None:
    assert_type(Group.objects, GroupManager[Group])
    assert_type(ProxyGroup.objects, GroupManager[ProxyGroup])
    assert_type(ProxyGroup.objects.get(), ProxyGroup)
    assert_type(ProxyGroup.objects.filter(), QuerySet[ProxyGroup])
    assert_type(ProxyGroup.objects.get_by_natural_key("name"), ProxyGroup)


async def group_manager_async_is_bound_to_the_model() -> None:
    assert_type(await ProxyGroup.objects.aget_by_natural_key("name"), ProxyGroup)


def permission_manager_is_bound_to_the_model() -> None:
    assert_type(Permission.objects, PermissionManager[Permission])
    assert_type(ProxyPermission.objects.get(), ProxyPermission)
    assert_type(ProxyPermission.objects.filter(), QuerySet[ProxyPermission])
    assert_type(ProxyPermission.objects.get_by_natural_key("codename", "app", "model"), ProxyPermission)


def site_manager_is_bound_to_the_model() -> None:
    assert_type(Site.objects, SiteManager[Site])
    assert_type(ProxySite.objects.get(), ProxySite)
    assert_type(ProxySite.objects.get_by_natural_key("example.com"), ProxySite)
    assert_type(ProxySite.objects.get_current(), Site)


def log_entry_manager_is_bound_to_the_model() -> None:
    assert_type(LogEntry.objects, LogEntryManager[LogEntry])
    assert_type(ProxyLogEntry.objects.get(), ProxyLogEntry)
    assert_type(ProxyLogEntry.objects.log_actions(1, [], 1, single_object=True), ProxyLogEntry)
    assert_type(ProxyLogEntry.objects.log_actions(1, [], 1), list[ProxyLogEntry])
