from django.contrib.flatpages.models import FlatPage, _FlatPage_sites
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
assert_type(site.flatpage_set.through, type[_FlatPage_sites])
