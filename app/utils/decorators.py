# app/utils/decorators.py
import re
from functools import wraps
from flask import request, jsonify
import jwt
from app.config import Config
from app.repositories import UserRepository


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            request.user_id = data['user_id']
        except:
            return jsonify({'error': 'Token is invalid'}), 401

        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Aici ar trebui să verifici dacă userul este admin
        # Exemplu simplist:
        user = UserRepository.get_user_by_id(request.user_id)
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin privileges required'}), 403
        return f(*args, **kwargs)

    return decorated


def validate_json(schema):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Request must be JSON'}), 400

            data = request.get_json()
            errors = {}

            for field, rules in schema.items():
                if rules.get('required') and field not in data:
                    errors[field] = 'This field is required'
                    continue

                if field in data:
                    value = data[field]

                    if 'type' in rules and not isinstance(value, eval(rules['type'])):
                        errors[field] = f'Must be of type {rules["type"]}'

                    if 'minlength' in rules and len(value) < rules['minlength']:
                        errors[field] = f'Must be at least {rules["minlength"]} characters'

                    if 'regex' in rules and not re.match(rules['regex'], value):
                        errors[field] = 'Invalid format'

            if errors:
                return jsonify({'errors': errors}), 400

            return f(*args, **kwargs)

        return decorated

    return decorator