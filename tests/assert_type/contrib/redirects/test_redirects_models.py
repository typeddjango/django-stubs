from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from django.db.models import Manager
from typing_extensions import assert_type

redirect = Redirect()
assert_type(redirect.id, int)
assert_type(redirect.pk, int)
assert_type(redirect.site_id, int)
assert_type(redirect.old_path, str)
assert_type(redirect.new_path, str)
assert_type(redirect.site, Site)
assert_type(redirect.objects, Manager[Redirect])
