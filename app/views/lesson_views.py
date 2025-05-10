# app/views/lesson_views.py

from flask import request, jsonify
from app.repositories.lesson_repository import LessonRepository
from app.views import api_blueprint
from app.utils.decorators import token_required, admin_required


@api_blueprint.route('/lessons', methods=['GET'])
def get_lessons():
    language = request.args.get('language')
    difficulty = request.args.get('difficulty')

    if language and difficulty:
        lessons = LessonRepository.get_lessons_by_language_and_difficulty(language, difficulty)
    elif language:
        lessons = LessonRepository.get_lessons_by_language(language)
    elif difficulty:
        lessons = LessonRepository.get_lessons_by_difficulty(difficulty)
    else:
        lessons = LessonRepository.get_all_lessons()

    return jsonify([{
        'id': lesson.id,
        'title': lesson.title,
        'language': lesson.language,
        'difficulty': lesson.difficulty,
        'content': lesson.content
    } for lesson in lessons])


@api_blueprint.route('/lessons/<int:lesson_id>', methods=['GET'])
def get_lesson(lesson_id):
    lesson = LessonRepository.get_lesson_by_id(lesson_id)
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404

    return jsonify({
        'id': lesson.id,
        'title': lesson.title,
        'language': lesson.language,
        'difficulty': lesson.difficulty,
        'content': lesson.content
    })


@api_blueprint.route('/lessons', methods=['POST'])
@token_required
@admin_required
def create_lesson():
    data = request.get_json()
    lesson = LessonRepository.create_lesson(
        title=data['title'],
        content=data['content'],
        language=data['language'],
        difficulty=data['difficulty']
    )

    return jsonify({
        'message': 'Lesson created successfully',
        'lesson_id': lesson.id
    }), 201


@api_blueprint.route('/lessons/<int:lesson_id>', methods=['PUT'])
@token_required
@admin_required
def update_lesson(lesson_id):
    data = request.get_json()
    lesson = LessonRepository.update_lesson(lesson_id, **data)

    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404

    return jsonify({
        'message': 'Lesson updated successfully',
        'lesson_id': lesson.id
    })


@api_blueprint.route('/lessons/<int:lesson_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_lesson(lesson_id):
    if not LessonRepository.delete_lesson(lesson_id):
        return jsonify({'error': 'Lesson not found'}), 404

    return jsonify({'message': 'Lesson deleted successfully'})