from flask import current_app
from app.models.user import User
from typing import Dict, Any


class NotificationService:
    @staticmethod
    def send_notification(user_id: int, message: str) -> Dict[str, Any]:
        """Send a notification to user"""
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found!")

        current_app.logger.info(f"Notification sent to {user.email}: {message}")
        return {
            "status": "success",
            "message": "Notification sent",
            "user_id": user_id
        }

    @staticmethod
    def notify_lesson_completion(user_id: int, lesson_title: str) -> Dict[str, Any]:
        """Notify user about completed lesson"""
        message = f"Congratulations! You completed: {lesson_title}"
        return NotificationService.send_notification(user_id, message)