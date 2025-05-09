from flask import Blueprint, request
from app.controllers.auth_controller import AuthController
from app.utils.api_response import api_response

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint"""
    data = request.get_json()
    try:
        response = AuthController.register(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        return api_response(response, 201)
    except ValueError as e:
        return api_response({'error': str(e)}, 400)

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    try:
        response = AuthController.login(
            email=data['email'],
            password=data['password']
        )
        return api_response(response)
    except ValueError as e:
        return api_response({'error': str(e)}, 401)

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    response = AuthController.logout()
    return api_response(response)