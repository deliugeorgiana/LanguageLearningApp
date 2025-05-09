from flask import Blueprint, request, jsonify
from app.services.lesson_service import LessonService
from app.utils.api_response import api_response

lesson_bp = Blueprint('lessons', __name__)

@lesson_bp.route('/', methods=['GET'])
def get_all_lessons():
    """Get all lessons"""
    lessons = LessonService.get_all_lessons()
    return api_response({
        'lessons': [{
            'id': lesson.id,
            'title': lesson.title,
            'language': lesson.language,
            'difficulty': lesson.difficulty
        } for lesson in lessons]
    })

@lesson_bp.route('/<int:lesson_id>', methods=['GET'])
def get_lesson(lesson_id):
    """Get specific lesson"""
    lesson = LessonService.get_lesson(lesson_id)
    if not lesson:
        return api_response({'error': 'Lesson not found'}, 404)
    return api_response({
        'lesson': {
            'id': lesson.id,
            'title': lesson.title,
            'content': lesson.content,
            'language': lesson.language,
            'difficulty': lesson.difficulty
        }
    })

@lesson_bp.route('/', methods=['POST'])
def create_lesson():
    """Create new lesson"""
    data = request.get_json()
    try:
        lesson = LessonService.create_lesson(
            title=data['title'],
            content=data['content'],
            language=data['language'],
            difficulty=data['difficulty']
        )
        return api_response({
            'message': 'Lesson created',
            'lesson_id': lesson.id
        }, 201)
    except ValueError as e:
        return api_response({'error': str(e)}, 400)

@lesson_bp.route('/<int:lesson_id>', methods=['PUT'])
def update_lesson(lesson_id):
    """Update existing lesson"""
    data = request.get_json()
    lesson = LessonService.update_lesson(lesson_id, **data)
    if not lesson:
        return api_response({'error': 'Lesson not found'}, 404)
    return api_response({'message': 'Lesson updated'})

@lesson_bp.route('/<int:lesson_id>', methods=['DELETE'])
def delete_lesson(lesson_id):
    """Delete lesson"""
    if not LessonService.delete_lesson(lesson_id):
        return api_response({'error': 'Lesson not found'}, 404)
    return api_response({'message': 'Lesson deleted'})