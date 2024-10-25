from typing import Optional

import flet as ft

from src.models.student import Student
from src.views.base_view import BaseView
from src.views.flet_ui.admin_view import AdminView
from src.views.flet_ui.login_view import LoginView
from src.views.flet_ui.student_view import StudentView


class AppView(BaseView):
    """Main application view that handles navigation and state."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.current_view: Optional[ft.View] = None
        self.current_student: Optional[Student] = None

        # Initialize views
        self.login_view = LoginView(self)
        self.admin_view = AdminView(self)
        self.student_view = StudentView(self)

        # Set up page properties
        self.page.title = "University Application"
        self.page.window_width = 1000
        self.page.window_height = 800
        self.page.window_min_width = 800
        self.page.window_min_height = 600
        self.page.window_resizable = True
        self.page.window_maximizable = True
        self.page.window_minimizable = True

        # 设置页面布局和样式
        self.page.padding = 20
        self.page.spacing = 20
        self.page.scroll = ft.ScrollMode.ADAPTIVE
        self.page.theme_mode = ft.ThemeMode.LIGHT

        # 创建主容器以实现居中布局
        self.main_container = ft.Container(
            expand=True,
            alignment=ft.alignment.center,
        )

        # 将主容器添加到页面
        self.page.add(self.main_container)

    def initialize(self):
        """Initialize the application with the login view."""
        self.navigate_to_login()

    def navigate_to_login(self):
        """Switch to login view."""
        self.current_view = self.login_view
        self._update_view()

    def navigate_to_admin(self):
        """Switch to admin view."""
        self.current_view = self.admin_view
        self._update_view()

    def navigate_to_student(self, student: Student):
        """Switch to student view."""
        self.current_student = student
        self.current_view = self.student_view
        self._update_view(student)

    def _update_view(self, data=None):
        """Update the current view with proper layout."""
        # 清空主容器
        self.main_container.content = None

        # 创建新的内容容器
        content = ft.Container(
            content=ft.Column(
                controls=[],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            width=900,
            padding=20,
        )

        # 将内容容器添加到主容器
        self.main_container.content = content

        # 显示当前视图
        if self.current_view:
            self.current_view.display(data)

        self.page.update()

    def display(self, data=None):
        """Implement abstract display method."""
        # 由于 AppView 是一个容器视图，实际显示由当前活动的子视图处理
        if self.current_view:
            self.current_view.display(data)
        self.page.update()

    def display_error(self, message: str):
        """Display error dialog."""

        def close_dlg(_):
            dlg.open = False
            self.page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=close_dlg)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def display_success(self, message: str):
        """Display success snackbar."""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.colors.GREEN_700,
        )
        self.page.snack_bar.open = True
        self.page.update()

    def get_input(self, prompt: str) -> str:
        """Get user input via dialog."""
        result = None

        def close_dlg(e):
            nonlocal result
            result = text_field.value if e.control.text == "OK" else None
            dlg.open = False
            self.page.update()

        text_field = ft.TextField(
            label=prompt,
            width=300,
            autofocus=True
        )
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(prompt),
            content=text_field,
            actions=[
                ft.TextButton("Cancel", on_click=close_dlg),
                ft.TextButton("OK", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
        return result if result is not None else ""

    def confirm_action(self, message: str) -> bool:
        """Get user confirmation via dialog."""
        result = False

        def handle_response(e):
            nonlocal result
            result = e.control.text == "Yes"
            dlg.open = False
            self.page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirm Action"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("No", on_click=handle_response),
                ft.TextButton("Yes", on_click=handle_response),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
        return result
