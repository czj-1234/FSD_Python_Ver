from typing import Any

from src.models.student import Student
from src.models.subject import Subject
from src.views.cli.base_cli_view import BaseCliView


class SubjectCliView(BaseCliView):
    """CLI view for subject-related operations."""

    # Show the course system
    # 显示课程系统
    def display(self, data: Any = None):
        self.display_header("Subject Enrolment System")
        self.display_menu(
            [
                ("c", "change: Change password"),
                ("e", "enrol: Enrol in a subject"),
                ("r", "remove: Remove a subject"),
                ("s", "show: Show enrolled subjects"),
                ("x", "exit"),
            ]
        )

    def display_subjects(self, student: Student):
        """Display student's enrolled subjects."""
        # 显示学生的注册科目。
        if not student.subjects:
            print("No subjects enrolled.")
            return

        self.display_header("Enrolled Subjects")
        self.display_table(
            headers=["ID", "Mark", "Grade"],
            rows=[[s.id, f"{s.mark:.1f}", s.grade] for s in student.subjects],
            widths=[6, 6, 5],
        )
        print(f"\nAverage Mark: {student.get_average_mark():.1f}")

    def display_enrolment_result(self, subject: Subject):
        """Display result of subject enrolment."""
        # 显示受试者登记结果。
        print(f"Successfully enrolled in subject {subject.id}")
        print(f"Mark: {subject.mark:.1f}")
        print(f"Grade: {subject.grade}")
