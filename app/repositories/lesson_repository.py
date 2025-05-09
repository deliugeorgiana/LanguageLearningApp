from app.models.lesson import Lesson
from app import db

class LessonRepository:
    @staticmethod
    def create_lesson(title, content, language, difficulty):
        lesson = Lesson(
            title=title,
            content=content,
            language=language,
            difficulty=difficulty
        )
        db.session.add(lesson)
        db.session.commit()
        return lesson

    @staticmethod
    def get_lesson_by_id(lesson_id):
        return Lesson.query.get(lesson_id)

    @staticmethod
    def get_all_lessons():
        return Lesson.query.all()

    @staticmethod
    def update_lesson(lesson_id, **kwargs):
        lesson = Lesson.query.get(lesson_id)
        if not lesson:
            return None
        for key, value in kwargs.items():
            setattr(lesson, key, value)
        db.session.commit()
        return lesson

    @staticmethod
    def delete_lesson(lesson_id):
        lesson = Lesson.query.get(lesson_id)
        if lesson:
            db.session.delete(lesson)
            db.session.commit()
            return True
        return False