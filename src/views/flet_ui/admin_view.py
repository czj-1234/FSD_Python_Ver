import flet as ft
from typing import Dict, List

from ..base_view import BaseView
from ...controllers.admin_controller import AdminController
from ...models.student import Student


class AdminView(BaseView):
    """Admin view for managing students and viewing statistics."""

    def __init__(self, app_view):
        self.app_view = app_view
        self.page = app_view.page
        self.admin_controller = AdminController(self)

        # Create UI controls
        self.student_list = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Email")),
                ft.DataColumn(ft.Text("Average Mark")),
                ft.DataColumn(ft.Text("Status")),
            ],
            rows=[]
        )

    def display(self, data=None):
        """Display the admin view."""

        def handle_show_students(e):
            students = self.admin_controller.database.load_all_students()
            self.display_all_students(students)

        def handle_group_students(e):
            self.admin_controller.group_students()

        def handle_partition_students(e):
            self.admin_controller.partition_students()

        def handle_remove_student(e):
            student_id = self.get_input("Enter student ID to remove")
            if student_id:
                self.admin_controller.remove_student()
                handle_show_students(None)  # Refresh list

        def handle_clear_database(e):
            if self.confirm_action("Are you sure you want to clear all data?"):
                self.admin_controller.clear_database()
                handle_show_students(None)  # Refresh list

        def handle_back(e):
            self.app_view.navigate_to_login()

        # Create buttons
        show_button = ft.ElevatedButton(
            text="Show All Students",
            on_click=handle_show_students
        )
        group_button = ft.ElevatedButton(
            text="Group by Grade",
            on_click=handle_group_students
        )
        partition_button = ft.ElevatedButton(
            text="Partition Pass/Fail",
            on_click=handle_partition_students
        )
        remove_button = ft.ElevatedButton(
            text="Remove Student",
            on_click=handle_remove_student
        )
        clear_button = ft.ElevatedButton(
            text="Clear Database",
            color=ft.colors.RED,
            on_click=handle_clear_database
        )
        back_button = ft.TextButton(
            text="Back to Login",
            on_click=handle_back
        )

        # Create layout
        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Admin Dashboard", size=30),
                    ft.Row(
                        controls=[
                            show_button,
                            group_button,
                            partition_button,
                            remove_button,
                            clear_button,
                        ],
                        wrap=True,
                        spacing=10
                    ),
                    self.student_list,
                    back_button
                ],
                spacing=20
            )
        )

    def display_all_students(self, students: List[Student]):
        """Display all students in the data table."""
        self.student_list.rows.clear()
        for student in students:
            self.student_list.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(student.id)),
                        ft.DataCell(ft.Text(student.name)),
                        ft.DataCell(ft.Text(student.email)),
                        ft.DataCell(ft.Text(f"{student.get_average_mark():.1f}")),
                        ft.DataCell(ft.Text("PASS" if student.is_passing() else "FAIL")),
                    ]
                )
            )
        self.page.update()

    def display_grade_groups(self, grade_groups: Dict[str, List[Student]]):
        """Display students grouped by grade."""
        def close_dialog(e):
            dlg.open = False
            self.page.update()

        content = ft.Column(
            controls=[ft.Text("Students Grouped by Grade", size=20)],
            scroll=ft.ScrollMode.AUTO,
            spacing=10
        )

        for grade, students in sorted(grade_groups.items()):
            grade_text = ft.Text(f"\nGrade {grade}:", weight=ft.FontWeight.BOLD)
            content.controls.append(grade_text)

            for student in students:
                student_text = ft.Text(
                    f"  {student.name} (ID: {student.id})"
                )
                content.controls.append(student_text)

        dlg = ft.AlertDialog(
            title=ft.Text("Grade Groups"),
            content=content,
            actions=[
                ft.TextButton("Close", on_click=close_dialog)
            ],
        )

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def display_partitioned_students(self, passing: List[Student], failing: List[Student]):
        """Display students partitioned by pass/fail status."""
        def close_dialog(e):
            dlg.open = False
            self.page.update()

        content = ft.Column(
            controls=[
                ft.Text("Students by Pass/Fail Status", size=20),
                ft.Text("\nPassing Students:", weight=ft.FontWeight.BOLD)
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=10
        )

        for student in passing:
            content.controls.append(ft.Text(
                f"  {student.name} (ID: {student.id}) - {student.get_average_mark():.1f}%"
            ))

        content.controls.append(ft.Text("\nFailing Students:", weight=ft.FontWeight.BOLD))

        for student in failing:
            content.controls.append(ft.Text(
                f"  {student.name} (ID: {student.id}) - {student.get_average_mark():.1f}%"
            ))

        dlg = ft.AlertDialog(
            title=ft.Text("Pass/Fail Partition"),
            content=content,
            actions=[
                ft.TextButton("Close", on_click=close_dialog)
            ],
        )

        self.page.dialog = dlg
        dlg.open = True
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