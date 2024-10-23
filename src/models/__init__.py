"""Data models for the university application."""

from .base_model import BaseModel
from .database import Database
from .student import Student
from .subject import Subject

__all__ = ["BaseModel", "Student", "Subject", "Database"]
