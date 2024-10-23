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
                ft.DataColumn(ft.Text("Average")),
                ft.DataColumn(ft.Text("Status")),
                ft.DataColumn(ft.Text("Subjects")),
            ],
            column_spacing=20,
            heading_row_height=40,
            data_row_min_height=100,  # Minimum height for data rows
            data_row_max_height=200,  # Maximum height for data rows
            horizontal_margin=20,
            horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_400),
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

        # Create layout with scrolling container for the table
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
                    ft.Container(
                        content=self.student_list,
                        padding=ft.padding.all(20),
                        border=ft.border.all(1, ft.colors.GREY_400),
                        border_radius=10,
                        expand=True,  # Allow container to expand
                        height=400  # Fixed height for scrolling
                    ),
                    back_button
                ],
                spacing=20,
                expand=True  # Allow column to expand
            )
        )

    def _format_subject_details(self, student: Student) -> ft.Container:
        """Create a formatted container of subject information."""
        subject_rows = []

        if student.subjects:
            for subject in student.subjects:
                # Create row for each subject
                subject_info = ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Text(
                                    f"Subject {subject.id}",
                                    weight=ft.FontWeight.BOLD,
                                    size=14
                                ),
                                bgcolor=ft.colors.BLUE_GREY_50,
                                padding=5,
                                border_radius=3
                            )
                        ]),
                        ft.Row([
                            ft.Container(
                                content=ft.Row([
                                    ft.Text("Mark: "),
                                    ft.Text(
                                        f"{subject.mark:.1f}",
                                        color=self._get_mark_color(subject.mark),
                                        weight=ft.FontWeight.BOLD
                                    )
                                ]),
                                padding=5
                            ),
                            ft.Container(
                                content=ft.Row([
                                    ft.Text("Grade: "),
                                    ft.Text(
                                        subject.grade,
                                        color=self._get_grade_color(subject.grade),
                                        weight=ft.FontWeight.BOLD
                                    )
                                ]),
                                padding=5
                            )
                        ])
                    ]),
                    border=ft.border.all(1, ft.colors.GREY_300),
                    border_radius=5,
                    margin=ft.margin.only(bottom=5),
                    padding=5
                )
                subject_rows.append(subject_info)
        else:
            subject_rows.append(
                ft.Container(
                    content=ft.Text(
                        "No subjects enrolled",
                        italic=True,
                        color=ft.colors.GREY_700
                    ),
                    padding=10
                )
            )

        return ft.Container(
            content=ft.Column(
                controls=subject_rows,
                spacing=5,
                scroll=ft.ScrollMode.AUTO
            ),
            width=300  # Fixed width for subject column
        )

    def _get_mark_color(self, mark: float) -> str:
        """Get color based on mark value."""
        if mark >= 85:
            return ft.colors.GREEN
        elif mark >= 75:
            return ft.colors.BLUE
        elif mark >= 65:
            return ft.colors.ORANGE
        elif mark >= 50:
            return ft.colors.ORANGE_700
        return ft.colors.RED

    def _get_grade_color(self, grade: str) -> str:
        """Get color based on grade."""
        grade_colors = {
            'HD': ft.colors.GREEN,
            'D': ft.colors.BLUE,
            'C': ft.colors.ORANGE,
            'P': ft.colors.ORANGE_700,
            'Z': ft.colors.RED
        }
        return grade_colors.get(grade, ft.colors.BLACK)

    def display_all_students(self, students: List[Student]):
        """Display all students in the data table."""
        self.student_list.rows.clear()

        if not students:
            self.display_error("No students found")
            return

        for student in students:
            avg_mark = student.get_average_mark()
            is_passing = student.is_passing()

            self.student_list.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(student.id)),
                        ft.DataCell(ft.Text(student.name)),
                        ft.DataCell(ft.Text(student.email)),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(
                                    f"{avg_mark:.1f}",
                                    color=self._get_mark_color(avg_mark),
                                    weight=ft.FontWeight.BOLD
                                ),
                                padding=5
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(
                                    "PASS" if is_passing else "FAIL",
                                    color=ft.colors.WHITE,
                                    weight=ft.FontWeight.BOLD
                                ),
                                bgcolor=ft.colors.GREEN if is_passing else ft.colors.RED,
                                padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                border_radius=3
                            )
                        ),
                        ft.DataCell(self._format_subject_details(student)),
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