from django.contrib.flatpages.models import FlatPage, _FlatPage_sites
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
assert_type(FlatPage.sites.through.objects, Manager[_FlatPage_sites])

flat_page_sites = FlatPage.sites.through.objects.get()
assert_type(flat_page_sites.id, int)
assert_type(flat_page_sites.pk, int)
assert_type(flat_page_sites.site, Site)
assert_type(flat_page_sites.site_id, int)
assert_type(flat_page_sites.flatpage, FlatPage)
assert_type(flat_page_sites.flatpage_id, int)
