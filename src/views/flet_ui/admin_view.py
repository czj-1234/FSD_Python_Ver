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
                ft.DataColumn(ft.Text("Subjects")),
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
                if self.admin_controller.remove_student(student_id):
                    handle_show_students(None)  # Refresh list

        def handle_clear_database(e):
            if self.confirm_action("Are you sure you want to clear all data?"):
                if self.admin_controller.clear_database():
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

    def _create_subject_text(self, student: Student) -> str:
        """Create a formatted string of subject information."""
        if not student.subjects:
            return "No subjects"

        subject_texts = []
        for subject in student.subjects:
            subject_texts.append(f"Subject {subject.id}: {subject.mark:.1f} ({subject.grade})")
        return "\n".join(subject_texts)

    def display_all_students(self, students: List[Student]):
        """Display all students in the data table."""
        self.student_list.rows.clear()

        if not students:
            self.display_error("No students found")
            return

        for student in students:
            self.student_list.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(student.id)),
                        ft.DataCell(ft.Text(student.name)),
                        ft.DataCell(ft.Text(student.email)),
                        ft.DataCell(ft.Text(f"{student.get_average_mark():.1f}")),
                        ft.DataCell(ft.Text(
                            "PASS" if student.is_passing() else "FAIL",
                            color=ft.colors.GREEN if student.is_passing() else ft.colors.RED
                        )),
                        ft.DataCell(ft.Text(self._create_subject_text(student))),
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
            controls=[ft.Text("Students Grouped by Average Grade", size=20)],
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
            height=400
        )

        # Sort grades in a specific order: HD, D, C, P, Z
        grade_order = ['HD', 'D', 'C', 'P', 'Z']

        for grade in grade_order:
            if grade in grade_groups and grade_groups[grade]:
                # Add grade header
                content.controls.append(
                    ft.Container(
                        content=ft.Text(
                            f"Grade {grade}",
                            size=18,
                            weight=ft.FontWeight.BOLD
                        ),
                        bgcolor=ft.colors.BLUE_GREY_100,
                        padding=10,
                        border_radius=5
                    )
                )

                # Add students in this grade group
                for student in grade_groups[grade]:
                    student_info = ft.Container(
                        content=ft.Column([
                            ft.Text(f"ID: {student.id}", weight=ft.FontWeight.BOLD),
                            ft.Text(f"Name: {student.name}"),
                            ft.Text(f"Email: {student.email}"),
                            ft.Text(f"Average Mark: {student.get_average_mark():.1f}"),
                            ft.Text("Subjects:", weight=ft.FontWeight.BOLD),
                            ft.Column([
                                ft.Text(
                                    f"  Subject {subject.id}: Mark = {subject.mark:.1f}, Grade = {subject.grade}"
                                ) for subject in student.subjects
                            ], spacing=2)
                        ]),
                        padding=10,
                        border=ft.border.all(1, ft.colors.GREY_400),
                        border_radius=5,
                        margin=ft.margin.only(bottom=10)
                    )
                    content.controls.append(student_info)

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
            controls=[ft.Text("Students by Pass/Fail Status", size=20)],
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
            height=400
        )

        # Helper function to create student info container
        def create_student_container(student: Student, status: str):
            return ft.Container(
                content=ft.Column([
                    ft.Text(f"ID: {student.id}", weight=ft.FontWeight.BOLD),
                    ft.Text(f"Name: {student.name}"),
                    ft.Text(f"Email: {student.email}"),
                    ft.Text(
                        f"Average Mark: {student.get_average_mark():.1f}",
                        color=ft.colors.GREEN if status == "Passing" else ft.colors.RED
                    ),
                    ft.Text("Subjects:", weight=ft.FontWeight.BOLD),
                    ft.Column([
                        ft.Text(
                            f"  Subject {subject.id}: Mark = {subject.mark:.1f}, Grade = {subject.grade}"
                        ) for subject in student.subjects
                    ], spacing=2)
                ]),
                padding=10,
                border=ft.border.all(1, ft.colors.GREY_400),
                border_radius=5,
                margin=ft.margin.only(bottom=10)
            )

        # Add passing students
        content.controls.append(
            ft.Container(
                content=ft.Text("Passing Students", size=18, weight=ft.FontWeight.BOLD),
                bgcolor=ft.colors.GREEN_100,
                padding=10,
                border_radius=5
            )
        )
        for student in passing:
            content.controls.append(create_student_container(student, "Passing"))

        # Add failing students
        content.controls.append(
            ft.Container(
                content=ft.Text("Failing Students", size=18, weight=ft.FontWeight.BOLD),
                bgcolor=ft.colors.RED_100,
                padding=10,
                border_radius=5
            )
        )
        for student in failing:
            content.controls.append(create_student_container(student, "Failing"))

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