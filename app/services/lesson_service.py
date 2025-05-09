from app.repositories.lesson_repository import LessonRepository
from app.models.lesson import Lesson
from typing import List, Optional, Dict, Any

class LessonService:
    @staticmethod
    def create_lesson(title: str, content: str, language: str, difficulty: str) -> Lesson:
        """Create a new lesson"""
        return LessonRepository.create_lesson(title, content, language, difficulty)

    @staticmethod
    def get_lesson(lesson_id: int) -> Optional[Lesson]:
        """Get a lesson by ID"""
        return LessonRepository.get_lesson_by_id(lesson_id)

    @staticmethod
    def get_all_lessons() -> List[Lesson]:
        """Get all lessons"""
        return LessonRepository.get_all_lessons()

    @staticmethod
    def update_lesson(lesson_id: int, **kwargs) -> Optional[Lesson]:
        """Update lesson details"""
        return LessonRepository.update_lesson(lesson_id, **kwargs)

    @staticmethod
    def delete_lesson(lesson_id: int) -> bool:
        """Delete a lesson"""
        return LessonRepository.delete_lesson(lesson_id)

    @staticmethod
    def search_lessons(query: str, language: Optional[str] = None) -> List[Lesson]:
        """Search lessons by title/content"""
        return LessonRepository.search_lessons(query, language)