import flet as ft
from typing import Optional

from ..base_view import BaseView
from ...controllers.subject_controller import SubjectController
from ...models.student import Student
from ...core.constants import PASSWORD_PATTERN


class StudentView(BaseView):
    """Student view for managing enrollments and account."""

    def __init__(self, app_view):
        self.app_view = app_view
        self.page = app_view.page
        self.subject_controller = SubjectController(self)
        self.current_student: Optional[Student] = None

        # Create UI controls
        self.subjects_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Mark")),
                ft.DataColumn(ft.Text("Grade")),
            ],
            rows=[]
        )

    def display(self, student: Student):
        """Display the student view."""
        self.current_student = student
        self.subject_controller.current_student = student

        def handle_enroll(e):
            if len(student.subjects) >= Student.MAX_SUBJECTS:
                self.display_error(f"Maximum subjects ({Student.MAX_SUBJECTS}) already enrolled!")
                return
            self.subject_controller.enrol_subject()
            self._refresh_subjects()

        def handle_remove(e):
            subject_id = self.get_input("Enter subject ID to remove")
            if subject_id:
                if self.subject_controller.remove_subject():
                    self._refresh_subjects()

        def handle_change_password(e):
            new_password = self.get_input("Enter new password")
            if new_password:
                if not PASSWORD_PATTERN.match(new_password):
                    self.display_error(
                        "Invalid password format! Must start with uppercase, contain at least 5 letters followed by 3+ digits")
                    return

                self.current_student.password = new_password
                if self.subject_controller.database.update_student(self.current_student):
                    self.display_success("Password changed successfully!")
                else:
                    self.display_error("Failed to change password!")

        def handle_logout(e):
            self.app_view.navigate_to_login()

        # Create layout
        self.page.clean()
        self.page.add(
            ft.Column(
                controls=[
                    ft.Text(f"Welcome, {student.name}!", size=30),
                    ft.Text(f"Student ID: {student.id}"),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                text="Enroll in Subject",
                                on_click=handle_enroll
                            ),
                            ft.ElevatedButton(
                                text="Remove Subject",
                                on_click=handle_remove
                            ),
                            ft.ElevatedButton(
                                text="Change Password",
                                on_click=handle_change_password
                            ),
                        ],
                        spacing=10
                    ),
                    ft.Text("Enrolled Subjects:", size=20),
                    self.subjects_table,
                    ft.TextButton(
                        text="Logout",
                        on_click=handle_logout
                    )
                ],
                spacing=20
            )
        )

        self._refresh_subjects()

    def _refresh_subjects(self):
        """Refresh the subjects table."""
        self.subjects_table.rows.clear()

        for subject in self.current_student.subjects:
            self.subjects_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(subject.id)),
                        ft.DataCell(ft.Text(f"{subject.mark:.1f}")),
                        ft.DataCell(ft.Text(subject.grade)),
                    ]
                )
            )

        if self.current_student.subjects:
            avg_mark = self.current_student.get_average_mark()
            status = "PASS" if self.current_student.is_passing() else "FAIL"
            self.subjects_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Average", italic=True)),
                        ft.DataCell(ft.Text(f"{avg_mark:.1f}", italic=True)),
                        ft.DataCell(ft.Text(status, color=ft.colors.GREEN if status == "PASS" else ft.colors.RED)),
                    ]
                )
            )

        self.page.update()

    def display_enrolment_result(self, subject):
        """Display the result of subject enrollment."""
        def close_dialog(e):
            self.page.dialog.open = False
            self.page.update()

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
                ft.TextButton("Close", on_click=close_dialog)
            ],
        )
        self.page.dialog.open = True
        self.page.update()

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