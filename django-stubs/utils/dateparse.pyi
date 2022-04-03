from datetime import date
from datetime import datetime as builtin_datetime
from datetime import time, timedelta
from typing import Optional, Pattern

date_re: Pattern[str]
time_re: Pattern[str]
datetime_re: Pattern[str]
standard_duration_re: Pattern[str]
iso8601_duration_re: Pattern[str]
postgres_interval_re: Pattern[str]

def parse_date(value: str) -> Optional[date]: ...
def parse_time(value: str) -> Optional[time]: ...
def parse_datetime(value: str) -> Optional[builtin_datetime]: ...
def parse_duration(value: str) -> Optional[timedelta]: ...
