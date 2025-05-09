from flask import request
from app.services.lesson_service import LessonService
from app.utils.api_response import api_response
from app.utils.validators import validate_lesson_data

class LessonController:
    @staticmethod
    def get_all_lessons():
        """Get all lessons"""
        lessons = LessonService.get_all_lessons()
        return api_response(
            data={"lessons": [lesson.to_dict() for lesson in lessons]},
            message="Lessons retrieved successfully"
        )

    @staticmethod
    def get_lesson(lesson_id: int):
        """Get a specific lesson"""
        lesson = LessonService.get_lesson(lesson_id)
        if not lesson:
            return api_response(
                status="error",
                message="Lesson not found",
                status_code=404
            )
        return api_response(
            data={"lesson": lesson.to_dict()},
            message="Lesson retrieved successfully"
        )

    @staticmethod
    def create_lesson(data: dict):
        """Create a new lesson"""
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
    def update_lesson(lesson_id: int, data: dict):
        """Update an existing lesson"""
        try:
            validate_lesson_data(data)
            lesson = LessonService.update_lesson(lesson_id, **data)
            if not lesson:
                return api_response(
                    status="error",
                    message="Lesson not found",
                    status_code=404
                )
            return api_response(
                message="Lesson updated successfully"
            )
        except ValueError as e:
            return api_response(
                status="error",
                message=str(e),
                status_code=400
            )

    @staticmethod
    def delete_lesson(lesson_id: int):
        """Delete a lesson"""
        success = LessonService.delete_lesson(lesson_id)
        if not success:
            return api_response(
                status="error",
                message="Lesson not found",
                status_code=404
            )
        return api_response(
            message="Lesson deleted successfully"
        )