import random
from typing import List

from src.models.base_model import BaseModel
from src.models.subject import Subject


class Student(BaseModel):
    """Represents a university student."""

    MAX_SUBJECTS = 4

    def __init__(self, name: str, email: str, password: str):
        """Initialize a new student."""
        self.id = f"{random.randint(1, 999999):06d}"
        self.name = name
        self.email = email
        self.password = password
        self.subjects: List[Subject] = []

    def enrol_subject(self, subject: Subject) -> bool:
        """Enrol in a new subject if not already at maximum."""
        if len(self.subjects) >= self.MAX_SUBJECTS:
            return False
        self.subjects.append(subject)
        return True

    def remove_subject(self, subject_id: str) -> bool:
        """Remove a subject from enrollment by ID."""
        initial_length = len(self.subjects)
        self.subjects = [s for s in self.subjects if s.id != subject_id]
        return len(self.subjects) < initial_length

    def get_average_mark(self) -> float:
        """Calculate average mark across all enrolled subjects."""
        if not self.subjects:
            return 0.0
        return sum(s.mark for s in self.subjects) / len(self.subjects)

    def is_passing(self) -> bool:
        """Determine if student is passing based on average mark."""
        return self.get_average_mark() >= 50

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "subjects": [s.to_dict() for s in self.subjects],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        student = cls(data["name"], data["email"], data["password"])
        student.id = data["id"]
        student.subjects = [Subject.from_dict(s) for s in data["subjects"]]
        return student
