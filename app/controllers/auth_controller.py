from flask import request
from app.services.auth_service import AuthService
from app.utils.api_response import api_response
from app.utils.validators import validate_email, validate_password


class AuthController:
    @staticmethod
    def register(username: str, email: str, password: str):
        """Handle user registration"""
        try:
            # Validate inputs
            if not validate_email(email):
                raise ValueError("Invalid email format")
            if not validate_password(password):
                raise ValueError("Password must be at least 8 characters")

            user = AuthService.register(username, email, password)
            return api_response(
                data={"user_id": user.id, "username": user.username},
                message="User registered successfully",
                status_code=201
            )
        except ValueError as e:
            return api_response(
                status="error",
                message=str(e),
                status_code=400
            )

    @staticmethod
    def login(email: str, password: str):
        """Handle user login"""
        try:
            user = AuthService.login(email, password)
            token = user.generate_auth_token()
            return api_response(
                data={
                    "user_id": user.id,
                    "token": token,
                    "is_admin": user.is_admin
                },
                message="Login successful"
            )
        except ValueError as e:
            return api_response(
                status="error",
                message=str(e),
                status_code=401
            )

    @staticmethod
    def logout():
        """Handle user logout"""
        # In a real app, you would invalidate the token here
        return api_response(message="Logout successful")