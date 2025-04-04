from datetime import datetime

from django.contrib.sessions.models import Session, SessionManager
from typing_extensions import assert_type

session = Session()
assert_type(session.session_key, str)
assert_type(session.pk, str)
assert_type(session.session_data, str)
assert_type(session.expire_date, datetime)
assert_type(session.objects, SessionManager[Session])
