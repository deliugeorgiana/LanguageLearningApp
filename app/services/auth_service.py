from werkzeug.security import generate_password_hash, check_password_hash
from app.repositories.user_repository import UserRepository
from app.models.user import User
from typing import Optional


class AuthService:
    @staticmethod
    def register_user(username: str, email: str, password: str) -> User:
        """Register a new user"""
        if UserRepository.get_user_by_email(email):
            raise ValueError("Email already in use!")

        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password_hash=hashed_password)
        UserRepository.save_user(user)
        return user

    @staticmethod
    def login_user(email: str, password: str) -> Optional[User]:
        """Authenticate a user"""
        user = UserRepository.get_user_by_email(email)
        if not user or not check_password_hash(user.password_hash, password):
            raise ValueError("Invalid credentials!")
        return user

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """Get user by ID"""
        return UserRepository.get_user_by_id(user_id)