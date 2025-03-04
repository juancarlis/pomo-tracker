from dataclasses import dataclass


@dataclass
class Category:
    id: int
    name: str
    color: str

    def __repr__(self) -> str:
        return f"({self.id}, {self.name}, {self.color})"
