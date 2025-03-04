import datetime


class Task:
    def __init__(
        self,
        id=None,
        description="",
        category_id=None,
        date_added=None,
        date_completed=None,
        status=None,
        position=None,
    ) -> None:
        self.id = id
        self.description = description
        self.category_id = category_id
        self.date_added = (
            date_added
            if date_added is not None
            else datetime.datetime.now().isoformat()
        )
        self.date_completed = date_completed if date_completed is not None else None
        self.status = status if status is not None else 0  # 0 = pending, 1 = completed
        self.position = position if position is not None else None

    def __repr__(self) -> str:
        return f"({self.description}, {self.category_id}, {self.date_added}, {self.date_completed}, {self.status}, {self.position})"
