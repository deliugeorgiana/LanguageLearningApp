# app/views/auth_views.py
import datetime

from flask import request, jsonify
from werkzeug.security import generate_password_hash
from app.repositories.user_repository import UserRepository
from app.views import api_blueprint
from app.utils.decorators import validate_json
from app.utils.security import generate_auth_token, verify_auth_token
import re

# Configurații
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
MIN_PASSWORD_LENGTH = 6


@api_blueprint.route('/register', methods=['POST'])
@validate_json({
    'username': {'type': 'string', 'required': True, 'minlength': 3},
    'email': {'type': 'string', 'required': True, 'regex': EMAIL_REGEX},
    'password': {'type': 'string', 'required': True, 'minlength': MIN_PASSWORD_LENGTH}
})
def register():
    data = request.get_json()

    # Verifică dacă utilizatorul există deja
    if UserRepository.get_user_by_username(data['username']):
        return jsonify({
            'error': 'Username already exists',
            'code': 'USERNAME_EXISTS'
        }), 400

    if UserRepository.get_user_by_email(data['email']):
        return jsonify({
            'error': 'Email already registered',
            'code': 'EMAIL_EXISTS'
        }), 400

    try:
        # Creează utilizatorul
        user = UserRepository.create_user({
            'username': data['username'],
            'email': data['email'],
            'password_hash': generate_password_hash(data['password']),
            'is_active': True
        })

        # Generează token JWT
        token = generate_auth_token(user.id)

        return jsonify({
            'message': 'Registration successful',
            'token': token,
            'user_id': user.id,
            'username': user.username
        }), 201

    except Exception as e:
        return jsonify({
            'error': 'Registration failed',
            'details': str(e),
            'code': 'REGISTRATION_ERROR'
        }), 500


@api_blueprint.route('/login', methods=['POST'])
@validate_json({
    'username_or_email': {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True}
})
def login():
    data = request.get_json()

    try:
        # Încearcă autentificarea
        user = UserRepository.authenticate_user(
            data['username_or_email'],
            data['password']
        )

        if not user:
            return jsonify({
                'error': 'Invalid credentials',
                'code': 'INVALID_CREDENTIALS'
            }), 401

        # Generează token nou
        token = generate_auth_token(user.id)

        # Actualizează ultima autentificare
        UserRepository.update_user(user.id, {'last_login': datetime.utcnow()})

        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user_id': user.id,
            'username': user.username
        })

    except Exception as e:
        return jsonify({
            'error': 'Login failed',
            'details': str(e),
            'code': 'LOGIN_ERROR'
        }), 500


@api_blueprint.route('/logout', methods=['POST'])
def logout():
    # În implementarea reală, ai nevoie de invalidarea token-ului
    return jsonify({'message': 'Logout successful'})


@api_blueprint.route('/me', methods=['GET'])
def get_current_user():
    # Exemplu de endpoint protejat care necesită autentificare
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid token'}), 401

    token = auth_header.split(' ')[1]
    user_id = verify_auth_token(token)

    if not user_id:
        return jsonify({'error': 'Invalid or expired token'}), 401

    user = UserRepository.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'user_id': user.id,
        'username': user.username,
        'email': user.email
    })


# Utilitare suplimentare
@api_blueprint.route('/check-username/<username>', methods=['GET'])
def check_username(username):
    exists = UserRepository.get_user_by_username(username) is not None
    return jsonify({'available': not exists})


@api_blueprint.route('/check-email/<email>', methods=['GET'])
def check_email(email):
    if not re.match(EMAIL_REGEX, email):
        return jsonify({'valid': False, 'message': 'Invalid email format'})

    exists = UserRepository.get_user_by_email(email) is not None
    return jsonify({'available': not exists, 'valid': True})