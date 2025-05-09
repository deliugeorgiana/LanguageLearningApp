import re
from typing import Dict, Optional
from datetime import datetime


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> Optional[str]:
    """Validate password requirements"""
    if len(password) < 8:
        return "Password must be at least 8 characters"
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one digit"
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase letter"
    return None


def validate_lesson_data(data: Dict) -> Optional[str]:
    """Validate lesson creation/update data"""
    required_fields = ['title', 'content', 'language', 'difficulty']
    for field in required_fields:
        if field not in data or not data[field]:
            return f"Field '{field}' is required"

    if len(data['title']) > 100:
        return "Title too long (max 100 characters)"

    if data['difficulty'] not in ['beginner', 'intermediate', 'advanced']:
        return "Invalid difficulty level"

    return None


def validate_progress_data(score: float) -> Optional[str]:
    """Validate progress tracking data"""
    if not 0 <= score <= 100:
        return "Score must be between 0 and 100"
    return None