from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class ActivitySession:
    application: str
    pid: int
    window_handle: int
    window_title: str
    start_time: datetime
    end_time: datetime
    duration: timedelta
