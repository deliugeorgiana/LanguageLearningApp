# app/views/progress_views.py

from flask import request, jsonify
from app.repositories.progress_repository import ProgressRepository
from app.views import api_blueprint
from app.utils.decorators import token_required


@api_blueprint.route('/progress', methods=['POST'])
@token_required
def save_progress():
    data = request.get_json()
    user_id = request.user_id  # Obținut din decoratorul token_required

    progress = ProgressRepository.save_progress(
        user_id=user_id,
        lesson_id=data['lesson_id'],
        score=data['score']
    )

    return jsonify({
        'message': 'Progress saved successfully',
        'progress_id': progress.id
    }), 201


@api_blueprint.route('/progress', methods=['GET'])
@token_required
def get_user_progress():
    user_id = request.user_id
    progress = ProgressRepository.get_user_progress(user_id)

    return jsonify([{
        'lesson_id': p.lesson_id,
        'score': p.score,
        'completed_at': p.completed_at.isoformat() if p.completed_at else None
    } for p in progress])


@api_blueprint.route('/progress/<int:lesson_id>', methods=['GET'])
@token_required
def get_lesson_progress(lesson_id):
    user_id = request.user_id
    progress = ProgressRepository.get_lesson_progress(user_id, lesson_id)

    if not progress:
        return jsonify({'error': 'Progress not found'}), 404

    return jsonify({
        'lesson_id': progress.lesson_id,
        'score': progress.score,
        'completed_at': progress.completed_at.isoformat() if progress.completed_at else None
    })


@api_blueprint.route('/progress/stats', methods=['GET'])
@token_required
def get_progress_stats():
    user_id = request.user_id
    average_score = ProgressRepository.get_average_score(user_id)
    total_lessons = ProgressRepository.get_total_completed(user_id)

    return jsonify({
        'average_score': average_score,
        'total_completed': total_lessons
    })