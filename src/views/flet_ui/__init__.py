"""Flet UI views for the university application."""

from .app_view import AppView
from .login_view import LoginView
from .admin_view import AdminView
from .student_view import StudentView
from .subject_view import SubjectView

__all__ = [
    'AppView',
    'LoginView',
    'AdminView',
    'StudentView',
    'SubjectView'
]