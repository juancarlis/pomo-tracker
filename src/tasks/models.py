from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    id: Optional[int] = None
    title: str = ""
    category_id: Optional[int] = None
    date_added: str = field(default_factory=lambda: datetime.now().isoformat())
    date_completed: Optional[str] = None
    status: int = 0
    position: Optional[int] = None

    def __post_init__(self):
        """Asegura que los valores sean correctos"""
        self.date_completed = self.date_completed or None
        self.status = self.status or 0
        self.position = self.position or None


@dataclass
class PendingTaskDTO:
    position: Optional[int]
    title: str
    category_name: str
    date_added: str
    tracking: int = 0
