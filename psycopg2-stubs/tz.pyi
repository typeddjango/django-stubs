import datetime

ZERO = datetime.timedelta(0)

class FixedOffsetTimezone(datetime.tzinfo): ...

STDOFFSET: datetime.timedelta
DSTOFFSET: datetime.timedelta
DSTDIFF: datetime.timedelta

class LocalTimezone(datetime.tzinfo): ...

LOCAL: LocalTimezone
