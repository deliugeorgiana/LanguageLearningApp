from werkzeug.security import generate_password_hash as werkzeug_generate_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from typing import Optional

def generate_password_hash(password: str) -> str:
    """Generate a secure password hash using werkzeug"""
    return werkzeug_generate_hash(password)

def verify_password(password_hash: str, password: str) -> bool:
    """Verify if password matches the hash"""
    return check_password_hash(password_hash, password)

def generate_auth_token(user_id: int, expiration: int = 3600) -> str:
    """Generate JWT authentication token"""
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'user_id': user_id}).decode('utf-8')

def verify_auth_token(token: str) -> Optional[int]:
    """Verify JWT token and return user_id if valid"""
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
        return data['user_id']
    except:
        return None

def get_password_hash(password: str) -> str:
    """Wrapper for password hash generation"""
    return generate_password_hash(password)