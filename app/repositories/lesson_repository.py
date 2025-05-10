# app/repositories/lesson_repository.py

from app.models.lesson import Lesson
from app import db


class LessonRepository:
    @staticmethod
    def create_lesson(title, content, language, difficulty):
        """
        Create a new lesson in the database.

        Args:
            title: Lesson title
            content: Lesson content
            language: Language of the lesson
            difficulty: Difficulty level

        Returns:
            The created Lesson object
        """
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
        """
        Get a lesson by its ID.

        Args:
            lesson_id: ID of the lesson to retrieve

        Returns:
            Lesson object or None if not found
        """
        return Lesson.query.get(lesson_id)

    @staticmethod
    def get_all_lessons():
        """
        Get all lessons in the database.

        Returns:
            List of all Lesson objects
        """
        return Lesson.query.all()

    @staticmethod
    def get_lessons_by_language(language):
        """
        Get all lessons for a specific language.

        Args:
            language: Language to filter by

        Returns:
            List of Lesson objects for the specified language
        """
        return Lesson.query.filter_by(language=language).all()

    @staticmethod
    def get_lessons_by_difficulty(difficulty):
        """
        Get all lessons for a specific difficulty level.

        Args:
            difficulty: Difficulty level to filter by

        Returns:
            List of Lesson objects for the specified difficulty
        """
        return Lesson.query.filter_by(difficulty=difficulty).all()

    @staticmethod
    def update_lesson(lesson_id, **kwargs):
        """
        Update a lesson's attributes.

        Args:
            lesson_id: ID of the lesson to update
            **kwargs: Attributes to update

        Returns:
            Updated Lesson object or None if not found
        """
        lesson = Lesson.query.get(lesson_id)
        if not lesson:
            return None
        for key, value in kwargs.items():
            setattr(lesson, key, value)
        db.session.commit()
        return lesson

    @staticmethod
    def delete_lesson(lesson_id):
        """
        Delete a lesson from the database.

        Args:
            lesson_id: ID of the lesson to delete

        Returns:
            True if deleted, False if not found
        """
        lesson = Lesson.query.get(lesson_id)
        if lesson:
            db.session.delete(lesson)
            db.session.commit()
            return True
        return False