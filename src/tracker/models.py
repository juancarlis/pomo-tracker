from datetime import datetime
from dataclasses import dataclass


@dataclass
class ActiveTimer:
    position: int
    task: str
    category: str
    start_time: datetime
    current_time: datetime
    elapsed_time_seconds: float
    elapsed_time_minutes: float
