from datetime import datetime
from dataclasses import dataclass


@dataclass
class ActiveTimer:
    position: int
    task: str
    category: str
    start_time: datetime
    current_time: datetime
    elapsed_time: str


@dataclass
class DailySummary:
    id: int
    task: str
    category: str
    minutes_elapsed: str
    hours_elapsed: str
    start_time: datetime
    end_time: datetime
