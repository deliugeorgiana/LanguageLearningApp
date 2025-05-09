from app.repositories.progress_repository import ProgressRepository
from app.models.progress import Progress
from typing import List, Optional

class ProgressService:
    @staticmethod
    def save_progress(user_id: int, lesson_id: int, score: float) -> Progress:
        """Save user progress for a lesson"""
        if not 0 <= score <= 100:
            raise ValueError("Score must be between 0 and 100")
        return ProgressRepository.save_progress(user_id, lesson_id, score)

    @staticmethod
    def get_user_progress(user_id: int) -> List[Progress]:
        """Get all progress entries for a user"""
        return ProgressRepository.get_user_progress(user_id)

    @staticmethod
    def get_lesson_progress(lesson_id: int) -> List[Progress]:
        """Get all progress entries for a lesson"""
        return ProgressRepository.get_lesson_progress(lesson_id)

    @staticmethod
    def get_user_lesson_progress(user_id: int, lesson_id: int) -> Optional[Progress]:
        """Get specific progress entry for user and lesson"""
        return ProgressRepository.get_user_lesson_progress(user_id, lesson_id)