from flask import request

from app.services.auth_service import AuthService
from app.services.lesson_service import LessonService
from app.utils.api_response import api_response
from app.utils.validators import validate_lesson_data

class AdminController:
    @staticmethod
    def create_lesson(data: dict):
        """Admin endpoint for creating lessons"""
        try:
            validate_lesson_data(data)
            lesson = LessonService.create_lesson(**data)
            return api_response(
                data={"lesson_id": lesson.id},
                message="Lesson created successfully",
                status_code=201
            )
        except ValueError as e:
            return api_response(
                status="error",
                message=str(e),
                status_code=400
            )

    @staticmethod
    def get_all_users():
        """Admin endpoint to get all users"""
        users = AuthService.get_all_users()
        return api_response(
            data={"users": [user.to_dict() for user in users]},
            message="Users retrieved successfully"
        )