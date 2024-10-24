from typing import Dict, List

import flet as ft

from src.controllers.admin_controller import AdminController
from src.models.student import Student
from src.views.base_view import BaseView


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
            data_row_min_height=100,
            data_row_max_height=200,
            horizontal_margin=20,
            horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_400),
            rows=[]
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

    def display(self, data=None):
        """Display the admin view."""

        def handle_show_students(e):
            self.page.show_loading = True
            self.page.update()
            try:
                students = self.admin_controller.database.load_all_students()
                self.display_all_students(students)
            finally:
                self.page.show_loading = False
                self.page.update()

        def handle_group_students(e):
            self.page.show_loading = True
            self.page.update()
            try:
                self.admin_controller.group_students()
            finally:
                self.page.show_loading = False
                self.page.update()

        def handle_partition_students(e):
            self.page.show_loading = True
            self.page.update()
            try:
                self.admin_controller.partition_students()
            finally:
                self.page.show_loading = False
                self.page.update()

        def handle_remove_student(e):
            def handle_remove_confirm(e):
                nonlocal student_id_field
                dialog.open = False
                self.page.update()

                student_id = student_id_field.value
                if student_id:
                    self.page.show_loading = True
                    self.page.update()
                    try:
                        if self.admin_controller.database.remove_student(student_id):
                            self.display_success(f"Student {student_id} removed successfully!")
                            handle_show_students(None)
                        else:
                            self.display_error(f"Student {student_id} not found!")
                    finally:
                        self.page.show_loading = False
                        self.page.update()

            def handle_remove_cancel(e):
                dialog.open = False
                self.page.update()

            student_id_field = ft.TextField(
                label="Student ID",
                hint_text="Enter student ID to remove",
                width=300
            )

            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Remove Student"),
                content=ft.Column([
                    ft.Text("Please enter the ID of the student to remove:"),
                    student_id_field,
                ], tight=True),
                actions=[
                    ft.TextButton("Cancel", on_click=handle_remove_cancel),
                    ft.TextButton("Remove", on_click=handle_remove_confirm),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            self.page.dialog = dialog
            dialog.open = True
            self.page.update()

        def handle_clear_database(e):
            def handle_clear_confirm(e):
                dialog.open = False
                self.page.update()

                self.page.show_loading = True
                self.page.update()
                try:
                    self.admin_controller.database.clear_all()
                    self.display_success("Database cleared successfully!")
                    self.student_list.rows.clear()
                    self.page.update()
                except Exception as ex:
                    self.display_error(f"Error clearing database: {str(ex)}")
                finally:
                    self.page.show_loading = False
                    self.page.update()

            def handle_clear_cancel(e):
                dialog.open = False
                self.page.update()

            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Clear Database"),
                content=ft.Text(
                    "Are you sure you want to clear all data? This action cannot be undone!"
                ),
                actions=[
                    ft.TextButton("Cancel", on_click=handle_clear_cancel),
                    ft.TextButton(
                        "Clear All",
                        on_click=handle_clear_confirm,
                        style=ft.ButtonStyle(
                            color={"": ft.colors.RED}
                        )
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            self.page.dialog = dialog
            dialog.open = True
            self.page.update()

        def handle_back(e):
            self.app_view.navigate_to_login()

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

        # 设置表格列的宽度和对齐方式
        self.student_list = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID"), numeric=False),
                ft.DataColumn(ft.Text("Name"), numeric=False),
                ft.DataColumn(ft.Text("Email"), numeric=False),
                ft.DataColumn(ft.Text("Average"), numeric=True),
                ft.DataColumn(ft.Text("Status"), numeric=False),
                ft.DataColumn(ft.Text("Subjects"), numeric=False),
            ],
            column_spacing=20,
            heading_row_height=40,
            data_row_min_height=100,
            data_row_max_height=200,
            horizontal_margin=20,
            horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_400),
            rows=[],
        )

        # 创建可滚动的表格容器
        table_container = ft.Container(
            content=self.student_list,
            padding=ft.padding.all(20),
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            expand=True,
            alignment=ft.alignment.center,  # 容器内容居中
        )

        # 创建按钮行
        button_row = ft.Container(
            content=ft.Row(
                controls=[
                    show_button,
                    group_button,
                    partition_button,
                    remove_button,
                    clear_button,
                ],
                wrap=True,
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.only(bottom=20),
        )

        # 创建主内容列
        main_column = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Admin Dashboard",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(bottom=20),
                ),
                button_row,
                ft.Container(
                    content=ft.Column(
                        controls=[table_container],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    ),
                    expand=True,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=back_button,
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(top=20),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )

        # 创建主容器
        main_content = ft.Container(
            content=main_column,
            expand=True,
            alignment=ft.alignment.center,
            padding=ft.padding.all(20),
            width=1200,  # 设置一个合适的固定宽度
        )

        # 更新主容器内容
        if hasattr(self.app_view, 'main_container'):
            self.app_view.main_container.content = main_content
        else:
            self.page.clean()
            self.page.add(main_content)

        self.page.update()

    def display_all_students(self, students: List[Student]):
        """Display all students in the data table."""
        self.student_list.rows.clear()

        if not students:
            self.display_error("No students found")
            return

        try:
            for student in students:
                avg_mark = student.get_average_mark()
                is_passing = student.is_passing()

                self.student_list.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(student.id),
                                    padding=ft.padding.all(5),
                                )
                            ),
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(student.name),
                                    padding=ft.padding.all(5),
                                )
                            ),
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(student.email),
                                    padding=ft.padding.all(5),
                                )
                            ),
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(
                                        f"{avg_mark:.1f}",
                                        color=self._get_mark_color(avg_mark),
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    padding=ft.padding.all(5),
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
                                    border_radius=3,
                                    alignment=ft.alignment.center,
                                )
                            ),
                            ft.DataCell(self._format_subject_details(student)),
                        ]
                    )
                )

        except Exception as e:
            self.display_error(f"Error displaying students: {str(e)}")
        finally:
            self.page.update()

    def _format_subject_details(self, student: Student) -> ft.Container:
        """Create a formatted container of subject information."""
        subject_rows = []

        if student.subjects:
            for subject in student.subjects:
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
            width=300
        )

    def display_grade_groups(self, grade_groups: Dict[str, List[Student]]):
        """Display students grouped by grade."""
        dialog = None

        def close_dialog(e):
            dialog.open = False
            self.page.update()

        content = ft.Column(
            controls=[ft.Text("Students Grouped by Average Grade", size=20)],
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
            height=400
        )

        try:
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

            dialog = ft.AlertDialog(
                title=ft.Text("Grade Groups"),
                content=content,
                actions=[
                    ft.TextButton("Close", on_click=close_dialog)
                ],
            )

            self.page.dialog = dialog
            dialog.open = True
            self.page.update()

        except Exception as e:
            self.display_error(f"Error displaying grade groups: {str(e)}")

    def display_partitioned_students(self, passing: List[Student], failing: List[Student]):
        """Display students partitioned by pass/fail status."""
        dialog = None

        def close_dialog(e):
            dialog.open = False
            self.page.update()

        content = ft.Column(
            controls=[ft.Text("Students by Pass/Fail Status", size=20)],
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
            height=400
        )

        try:
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

            dialog = ft.AlertDialog(
                title=ft.Text("Pass/Fail Partition"),
                content=content,
                actions=[
                    ft.TextButton("Close", on_click=close_dialog)
                ],
            )

            self.page.dialog = dialog
            dialog.open = True
            self.page.update()

        except Exception as e:
            self.display_error(f"Error displaying partitioned students: {str(e)}")

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
