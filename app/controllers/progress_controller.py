from flask import request
from app.services.progress_service import ProgressService
from app.utils.api_response import api_response
from app.utils.validators import validate_progress_data

class ProgressController:
    @staticmethod
    def save_progress(user_id: int, lesson_id: int, score: float):
        """Save user progress"""
        try:
            validate_progress_data(score)
            progress = ProgressService.save_progress(user_id, lesson_id, score)
            return api_response(
                data={"progress_id": progress.id},
                message="Progress saved successfully",
                status_code=201
            )
        except ValueError as e:
            return api_response(
                status="error",
                message=str(e),
                status_code=400
            )

    @staticmethod
    def get_user_progress(user_id: int):
        """Get progress for a specific user"""
        progress = ProgressService.get_user_progress(user_id)
        return api_response(
            data={"progress": [p.to_dict() for p in progress]},
            message="User progress retrieved successfully"
        )

    @staticmethod
    def get_lesson_progress(lesson_id: int):
        """Get progress for a specific lesson"""
        progress = ProgressService.get_lesson_progress(lesson_id)
        return api_response(
            data={"progress": [p.to_dict() for p in progress]},
            message="Lesson progress retrieved successfully"
        )