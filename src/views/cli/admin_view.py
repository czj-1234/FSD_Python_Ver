from typing import List, Dict, Any

from src.models.student import Student
from src.views.cli.base_cli_view import BaseCliView


class AdminCliView(BaseCliView):
    """CLI view for admin-related operations."""

    def display(self, data: Any = None):
        self.display_header("Admin System")
        self.display_menu(
            [
                ("c", "clear database: Clear all data"),
                ("g", "group students: Group by grade"),
                ("p", "partition students: Partition PASS/FAIL"),
                ("r", "remove student: Remove by ID"),
                ("s", "show: Show all students"),
                ("x", "exit"),
            ]
        )

    def display_all_students(self, students: List[Student]):
        """Display all students in the system."""
        if not students:
            print("No students found.")
            return

        self.display_header("All Students")
        self.display_table(
            headers=["ID", "Name", "Email"],
            rows=[[s.id, s.name[:20], s.email] for s in students],
            widths=[8, 20, 30],
        )

    def display_grade_groups(self, groups: Dict[str, List[Student]]):
        """Display students grouped by grade."""
        self.display_header("Students Grouped by Grade")
        for grade in sorted(groups.keys()):
            print(f"\nGrade {grade}:")
            self.display_table(
                headers=["ID", "Name", "Email"],
                rows=[[s.id, s.name[:20], s.email] for s in groups[grade]],
                widths=[8, 20, 30],
            )

    def display_partitioned_students(
            self, passing: List[Student], failing: List[Student]
    ):
        """Display students partitioned by pass/fail status."""
        self.display_header("Passing Students")
        self.display_table(
            headers=["ID", "Name", "Average Mark"],
            rows=[[s.id, s.name[:20], f"{s.get_average_mark():.1f}"] for s in passing],
            widths=[8, 20, 12],
        )

        print("\nFailing Students:")
        self.display_table(
            headers=["ID", "Name", "Average Mark"],
            rows=[[s.id, s.name[:20], f"{s.get_average_mark():.1f}"] for s in failing],
            widths=[8, 20, 12],
        )
