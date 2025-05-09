from flask import Blueprint, request
from app.services.progress_service import ProgressService
from app.utils.api_response import api_response

progress_bp = Blueprint('progress', __name__)

@progress_bp.route('/', methods=['POST'])
def save_progress():
    """Save user progress"""
    data = request.get_json()
    try:
        progress = ProgressService.save_progress(
            user_id=data['user_id'],
            lesson_id=data['lesson_id'],
            score=data['score']
        )
        return api_response({
            'message': 'Progress saved',
            'progress_id': progress.id
        }, 201)
    except ValueError as e:
        return api_response({'error': str(e)}, 400)

@progress_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_progress(user_id):
    """Get user progress"""
    progress = ProgressService.get_user_progress(user_id)
    return api_response({
        'progress': [{
            'lesson_id': p.lesson_id,
            'score': p.score,
            'completed_at': p.completed_at.isoformat()
        } for p in progress]
    })

@progress_bp.route('/lesson/<int:lesson_id>', methods=['GET'])
def get_lesson_progress(lesson_id):
    """Get progress for specific lesson"""
    progress = ProgressService.get_lesson_progress(lesson_id)
    return api_response({
        'progress': [{
            'user_id': p.user_id,
            'score': p.score,
            'completed_at': p.completed_at.isoformat()
        } for p in progress]
    })