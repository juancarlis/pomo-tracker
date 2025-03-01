import datetime


class Task:
    def __init__(
        self,
        description,
        category,
        date_added=None,
        date_completed=None,
        status=None,
        position=None,
    ) -> None:
        self.description = description
        self.category = category
        self.date_added = (
            date_added
            if date_added is not None
            else datetime.datetime.now().isoformat()
        )
        self.date_completed = date_completed if date_completed is not None else None
        self.status = status if status is not None else 0  # 0 = pending, 1 = completed
        self.position = position if position is not None else None

    def __repr__(self) -> str:
        return f"({self.description}, {self.category}, {self.date_added}, {self.date_completed}, {self.status}, {self.position})"
