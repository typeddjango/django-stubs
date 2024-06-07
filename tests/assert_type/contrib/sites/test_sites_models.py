from typing import Type

from django.contrib.flatpages.models import FlatPage, FlatPage_sites
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from typing_extensions import assert_type

site = Site()
assert_type(site.id, int)
assert_type(site.pk, int)
assert_type(site.domain, str)
assert_type(site.name, str)
assert_type(site.flatpage_set.get(), FlatPage)
assert_type(site.redirect_set.get(), Redirect)

# Pyright doesn't allow "runtime" usage of @type_check_only 'FlatPage_sites' but
# we're only type checking these files so it should be fine.
assert_type(site.flatpage_set.through, Type[FlatPage_sites])  # pyright: ignore[reportGeneralTypeIssues]
