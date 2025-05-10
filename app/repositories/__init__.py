# app/repositories/__init__.py

from .user_repository import UserRepository
from .lesson_repository import LessonRepository
from .progress_repository import ProgressRepository

__all__ = [
    'UserRepository',
    'LessonRepository',
    'ProgressRepository'
]