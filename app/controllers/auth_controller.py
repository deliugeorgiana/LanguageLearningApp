from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthController:
    @staticmethod
    def register(username, email, password):
        if UserRepository.get_by_email(email):
            raise ValueError('Email already exists')

        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)
        UserRepository.save(user)
        return {'message': 'User registered successfully'}

    @staticmethod
    def login(email, password):
        user = UserRepository.get_by_email(email)
        if not user or not check_password_hash(user.password, password):
            raise ValueError('Invalid credentials')

        # Aici poți adăuga logica pentru JWT token
        return {'message': 'Login successful', 'user_id': user.id}

    @staticmethod
    def logout():
        # Implementare logout
        return {'message': 'Logout successful'}