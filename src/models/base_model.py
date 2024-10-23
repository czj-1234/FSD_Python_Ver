import json
from abc import ABC, abstractmethod


class BaseModel(ABC):
    """Base class for all models providing common functionality."""

    @abstractmethod
    def to_dict(self) -> dict:
        """Convert model instance to dictionary for serialization."""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> "BaseModel":
        """Create model instance from dictionary."""
        pass

    def to_json(self) -> str:
        """Convert model instance to JSON string."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> "BaseModel":
        """Create model instance from JSON string."""
        return cls.from_dict(json.loads(json_str))
