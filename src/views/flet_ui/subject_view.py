import flet as ft
from typing import Optional

from ..base_view import BaseView
from ...models.student import Student
from ...models.subject import Subject


class SubjectView(BaseView):
    """View for displaying subject details and enrollment results."""

    def __init__(self, app_view):
        self.app_view = app_view
        self.page = app_view.page

    def display_enrolment_result(self, subject: Subject):
        """Display the result of subject enrollment."""
        content = ft.Column(
            controls=[
                ft.Text("Subject Enrollment Result", size=20),
                ft.Text(f"Subject ID: {subject.id}"),
                ft.Text(f"Mark: {subject.mark:.1f}"),
                ft.Text(f"Grade: {subject.grade}"),
            ],
            spacing=10
        )

        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Enrollment Successful"),
            content=content,
            actions=[
                ft.TextButton("Close", on_click=lambda e: setattr(self.page.dialog, 'open', False))
            ],
        )
        self.page.dialog.open = True
        self.page.update()

    def display_subjects(self, student: Student):
        """Display all subjects for a student."""
        content = ft.Column(
            controls=[ft.Text("Enrolled Subjects", size=20)],
            scroll=ft.ScrollMode.AUTO
        )

        if not student.subjects:
            content.controls.append(ft.Text("No subjects enrolled"))
        else:
            for subject in student.subjects:
                content.controls.append(
                    ft.Text(f"Subject {subject.id}: Mark = {subject.mark:.1f}, Grade = {subject.grade}")
                )

            avg_mark = student.get_average_mark()
            content.controls.extend([
                ft.Text(""),
                ft.Text(f"Average Mark: {avg_mark:.1f}"),
                ft.Text(f"Status: {'PASS' if student.is_passing() else 'FAIL'}")
            ])

        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Subject Details"),
            content=content,
            actions=[
                ft.TextButton("Close", on_click=lambda e: setattr(self.page.dialog, 'open', False))
            ],
        )
        self.page.dialog.open = True
        self.page.update()

    def display(self, data=None):
        """Display subject view (not used directly)."""
        pass

    def display_error(self, message: str):
        """Display error message."""
        self.app_view.display_error(message)

    def display_success(self, message: str):
        """Display success message."""
        self.app_view.display_success(message)

    def get_input(self, prompt: str) -> str:
        """Get user input."""
        return self.app_view.get_input(prompt)

    def confirm_action(self, message: str) -> bool:
        """Get user confirmation."""
        return self.app_view.confirm_action(message)