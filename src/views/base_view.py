from abc import ABC, abstractmethod
from typing import Any


class BaseView(ABC):
    """Base interface for all views."""

    @abstractmethod
    def display(self, data: Any = None):
        """Display the main view content."""
        pass

    @abstractmethod
    def display_error(self, message: str):
        """Display an error message."""
        pass

    @abstractmethod
    def display_success(self, message: str):
        """Display a success message."""
        pass

    @abstractmethod
    def get_input(self, prompt: str) -> str:
        """Get user input."""
        pass

    @abstractmethod
    def confirm_action(self, message: str) -> bool:
        """Get user confirmation."""
        pass
