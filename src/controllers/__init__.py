"""Controllers for the university application."""

from .admin_controller import AdminController
from .base_controller import BaseController
from .student_controller import StudentController
from .subject_controller import SubjectController
from .university_controller import UniversityController

__all__ = [
    'BaseController',
    'UniversityController',
    'StudentController',
    'SubjectController',
    'AdminController'
]
