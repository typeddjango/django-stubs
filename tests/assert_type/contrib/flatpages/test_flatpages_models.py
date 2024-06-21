from django.contrib.flatpages.models import FlatPage, FlatPage_sites
from django.contrib.sites.models import Site
from django.db.models import Manager
from typing_extensions import assert_type

flat_page = FlatPage()
assert_type(flat_page.id, int)
assert_type(flat_page.pk, int)
assert_type(flat_page.url, str)
assert_type(flat_page.title, str)
assert_type(flat_page.content, str)
assert_type(flat_page.enable_comments, bool)
assert_type(flat_page.template_name, str)
assert_type(flat_page.registration_required, bool)
assert_type(flat_page.sites.get(), Site)

# Pyright doesn't allow "runtime" usage of @type_check_only 'FlatPage_sites' but
# we're only type checking these files so it should be fine.
assert_type(FlatPage.sites.through.objects, Manager[FlatPage_sites])  # pyright: ignore[reportGeneralTypeIssues]
flat_page_sites = FlatPage.sites.through.objects.get()
assert_type(flat_page_sites.id, int)
assert_type(flat_page_sites.pk, int)
assert_type(flat_page_sites.site, Site)
assert_type(flat_page_sites.site_id, int)
assert_type(flat_page_sites.flatpage, FlatPage)
assert_type(flat_page_sites.flatpage_id, int)
