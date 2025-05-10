# app/repositories/user_repository.py

from app.utils.security import get_password_hash, verify_password
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from app.models.user import User, UserLanguage
from app import db

class UserRepository:
    """
    Repository for user-related database operations.
    """

    @staticmethod
    def create_user(user_data: Dict[str, Any]) -> User:
        """
        Create a new user in the database.

        Args:
            user_data: Dictionary with user data

        Returns:
            The created User object
        """
        # Hash password before saving
        if "password" in user_data:
            user_data["password_hash"] = get_password_hash(user_data.pop("password"))

        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """
        Get a user by ID.

        Args:
            user_id: ID of the user to retrieve

        Returns:
            User object or None if not found
        """
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """
        Get a user by email address.

        Args:
            email: Email address to search for

        Returns:
            User object or None if not found
        """
        return User.query.filter(User.email == email).first()

    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        """
        Get a user by username.

        Args:
            username: Username to search for

        Returns:
            User object or None if not found
        """
        return User.query.filter(User.username == username).first()

    @staticmethod
    def get_users(skip: int = 0, limit: int = 100, active_only: bool = True) -> List[User]:
        """
        Get a list of users with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            active_only: Whether to return only active users

        Returns:
            List of User objects
        """
        query = User.query
        if active_only:
            query = query.filter(User.is_active == True)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_user(user_id: int, update_data: Dict[str, Any]) -> Optional[User]:
        """
        Update a user's information.

        Args:
            user_id: ID of the user to update
            update_data: Dictionary with data to update

        Returns:
            Updated User object or None if not found
        """
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return None

        # Handle password if included in update
        if "password" in update_data:
            update_data["password_hash"] = get_password_hash(update_data.pop("password"))

        for key, value in update_data.items():
            setattr(user, key, value)

        db.session.commit()
        db.session.refresh(user)
        return user

    @staticmethod
    def delete_user(user_id: int) -> bool:
        """
        Delete a user from the database.

        Args:
            user_id: ID of the user to delete

        Returns:
            True if deleted, False if not found
        """
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return False

        db.session.delete(user)
        db.session.commit()
        return True

    @staticmethod
    def authenticate_user(username_or_email: str, password: str) -> Optional[User]:
        """
        Authenticate a user using username/email and password.

        Args:
            username_or_email: Username or email for authentication
            password: Password for authentication

        Returns:
            Authenticated User object or None if authentication fails
        """
        user = User.query.filter(
            or_(
                User.username == username_or_email,
                User.email == username_or_email
            )
        ).first()

        if not user or not verify_password(password, user.password_hash):
            return None

        return user

    @staticmethod
    def deactivate_user(user_id: int) -> Optional[User]:
        """
        Deactivate a user account.

        Args:
            user_id: ID of the user to deactivate

        Returns:
            Deactivated User object or None if not found
        """
        return UserRepository.update_user(user_id, {"is_active": False})

    @staticmethod
    def add_user_language(user_id: int, language_data: Dict[str, Any]) -> Optional[UserLanguage]:
        """
        Add a learning language for a user.

        Args:
            user_id: ID of the user
            language_data: Dictionary with language data

        Returns:
            Created UserLanguage object or None if user not found
        """
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return None

        language_data["user_id"] = user_id
        user_language = UserLanguage(**language_data)

        db.session.add(user_language)
        db.session.commit()
        db.session.refresh(user_language)
        return user_language

    @staticmethod
    def get_user_languages(user_id: int) -> List[UserLanguage]:
        """
        Get all learning languages for a user.

        Args:
            user_id: ID of the user

        Returns:
            List of UserLanguage objects for the user
        """
        return UserLanguage.query.filter(UserLanguage.user_id == user_id).all()

    @staticmethod
    def update_user_language(user_language_id: int, update_data: Dict[str, Any]) -> Optional[UserLanguage]:
        """
        Update a user's language information.

        Args:
            user_language_id: ID of the UserLanguage record
            update_data: Dictionary with data to update

        Returns:
            Updated UserLanguage object or None if not found
        """
        user_language = UserLanguage.query.get(user_language_id)
        if not user_language:
            return None

        for key, value in update_data.items():
            setattr(user_language, key, value)

        db.session.commit()
        db.session.refresh(user_language)
        return user_language

    @staticmethod
    def delete_user_language(user_language_id: int) -> bool:
        """
        Delete a user's language record.

        Args:
            user_language_id: ID of the UserLanguage record to delete

        Returns:
            True if deleted, False if not found
        """
        user_language = UserLanguage.query.get(user_language_id)
        if not user_language:
            return False

        db.session.delete(user_language)
        db.session.commit()
        return True

    @staticmethod
    def search_users(query: str, limit: int = 20) -> List[User]:
        """
        Search users by username, email, first name, or last name.

        Args:
            query: Search string
            limit: Maximum number of results to return

        Returns:
            List of User objects matching the search criteria
        """
        search_pattern = f"%{query}%"
        return User.query.filter(
            or_(
                User.username.ilike(search_pattern),
                User.email.ilike(search_pattern),
                User.first_name.ilike(search_pattern),
                User.last_name.ilike(search_pattern)
            )
        ).limit(limit).all()

    @staticmethod
    def count_users(active_only: bool = True) -> int:
        """
        Count the number of users in the database.

        Args:
            active_only: Whether to count only active users

        Returns:
            Number of users
        """
        query = User.query
        if active_only:
            query = query.filter(User.is_active == True)
        return query.count()