import flet as ft
from typing import Optional

from .login_view import LoginView
from .admin_view import AdminView
from .student_view import StudentView
from ..base_view import BaseView
from ...models.student import Student


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

        # Set up page
        self.page.title = "University Application"
        self.page.padding = 20
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window_width = 800
        self.page.window_height = 600
        self.page.window_resizable = False

    def initialize(self):
        """Initialize the application with the login view."""
        self.navigate_to_login()

    def navigate_to_login(self):
        """Switch to login view."""
        self.current_view = self.login_view
        self.page.clean()
        self.login_view.display()
        self.page.update()

    def navigate_to_admin(self):
        """Switch to admin view."""
        self.current_view = self.admin_view
        self.page.clean()
        self.admin_view.display()
        self.page.update()

    def navigate_to_student(self, student: Student):
        """Switch to student view."""
        self.current_student = student
        self.current_view = self.student_view
        self.page.clean()
        self.student_view.display(student)
        self.page.update()

    def display(self, data=None):
        """Display current view."""
        if self.current_view:
            self.current_view.display(data)

    def display_error(self, message: str):
        """Display error dialog."""

        def close_dlg(_):
            dlg.open = False
            self.page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=close_dlg)],
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def display_success(self, message: str):
        """Display success snackbar."""
        self.page.snack_bar = ft.SnackBar(content=ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()

    def get_input(self, prompt: str) -> str:
        """Get user input via dialog."""
        result = ""

        def close_dlg(e):
            nonlocal result
            result = text_field.value
            dlg.open = False
            self.page.update()

        text_field = ft.TextField(label=prompt)
        dlg = ft.AlertDialog(
            title=ft.Text(prompt),
            content=text_field,
            actions=[
                ft.TextButton("Cancel", on_click=close_dlg),
                ft.TextButton("OK", on_click=close_dlg),
            ],
        )

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
        return result

    def confirm_action(self, message: str) -> bool:
        """Get user confirmation via dialog."""
        result = False

        def handle_yes(e):
            nonlocal result
            result = True
            dlg.open = False
            self.page.update()

        def handle_no(e):
            nonlocal result
            result = False
            dlg.open = False
            self.page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Confirm"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("No", on_click=handle_no),
                ft.TextButton("Yes", on_click=handle_yes),
            ],
        )

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
        return result