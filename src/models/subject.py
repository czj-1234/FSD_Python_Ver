import random

from src.models.base_model import BaseModel


class Subject(BaseModel):
    """Represents a university subject with ID, mark and grade."""

    def __init__(self, subject_id: str = None, mark: float = None):
        """Initialize a new subject."""
        self.id = subject_id or f"{random.randint(1, 999):03d}"
        self.mark = mark or random.randint(25, 100)
        self.grade = self._calculate_grade()

    def _calculate_grade(self) -> str:
        """Calculate grade based on mark."""
        if self.mark >= 85:
            return "HD"
        elif self.mark >= 75:
            return "D"
        elif self.mark >= 65:
            return "C"
        elif self.mark >= 50:
            return "P"
        else:
            return "Z"

    def to_dict(self) -> dict:
        return {"id": self.id, "mark": self.mark, "grade": self.grade}

    @classmethod
    def from_dict(cls, data: dict) -> "Subject":
        subject = cls(data["id"], data["mark"])
        subject.grade = data["grade"]
        return subject
