from typing import Any

from src.views.cli.base_cli_view import BaseCliView


class UniversityCliView(BaseCliView):
    """CLI view for the main university system."""

    def display(self, data: Any = None):
        self.display_header("Welcome to the University System")
        self.display_menu([("A", "Admin"), ("S", "Student"), ("X", "Exit")])
