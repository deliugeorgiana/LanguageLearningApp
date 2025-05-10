# app/views/user_views.py

from flask import request, jsonify
from app.repositories.user_repository import UserRepository
from app.views import api_blueprint
from app.utils.decorators import token_required, admin_required


@api_blueprint.route('/users', methods=['GET'])
@token_required
@admin_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    users = UserRepository.get_users(
        skip=(page - 1) * per_page,
        limit=per_page
    )

    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_active': user.is_active
    } for user in users])


@api_blueprint.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    user = UserRepository.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_active': user.is_active
    })


@api_blueprint.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    data = request.get_json()
    user = UserRepository.update_user(user_id, data)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'message': 'User updated successfully',
        'user_id': user.id
    })


@api_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(user_id):
    if not UserRepository.delete_user(user_id):
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'message': 'User deleted successfully'})