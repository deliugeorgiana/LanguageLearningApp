from app.models.lesson import Lesson
from app.repositories.progress_repository import ProgressRepository
from typing import Optional

class AIService:
    @staticmethod
    def recommend_lesson(user_id: int) -> Optional[Lesson]:
        """Recommend a lesson based on user progress"""
        progress = ProgressRepository.get_user_progress(user_id)

        if not progress:
            return Lesson.query.filter_by(difficulty="beginner").first()

        last_lesson_id = progress[-1].lesson_id
        last_lesson = Lesson.query.get(last_lesson_id)

        if not last_lesson:
            return Lesson.query.filter_by(difficulty="beginner").first()

        if last_lesson.difficulty == "beginner":
            return Lesson.query.filter_by(difficulty="intermediate").first()
        elif last_lesson.difficulty == "intermediate":
            return Lesson.query.filter_by(difficulty="advanced").first()
        else:
            return Lesson.query.order_by(Lesson.id.desc()).first()