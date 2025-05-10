# app/repositories/progress_repository.py

from app.models.progress import Progress
from app import db


class ProgressRepository:
    @staticmethod
    def save_progress(user_id, lesson_id, score):
        """
        Save or update user progress for a lesson.

        Args:
            user_id: ID of the user
            lesson_id: ID of the lesson
            score: Score achieved

        Returns:
            The created/updated Progress object
        """
        # Check if progress already exists
        progress = Progress.query.filter_by(
            user_id=user_id,
            lesson_id=lesson_id
        ).first()

        if progress:
            progress.score = score
        else:
            progress = Progress(
                user_id=user_id,
                lesson_id=lesson_id,
                score=score
            )
            db.session.add(progress)

        db.session.commit()
        return progress

    @staticmethod
    def get_user_progress(user_id):
        """
        Get all progress records for a user.

        Args:
            user_id: ID of the user

        Returns:
            List of Progress objects for the user
        """
        return Progress.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_lesson_progress(user_id, lesson_id):
        """
        Get a user's progress for a specific lesson.

        Args:
            user_id: ID of the user
            lesson_id: ID of the lesson

        Returns:
            Progress object or None if not found
        """
        return Progress.query.filter_by(
            user_id=user_id,
            lesson_id=lesson_id
        ).first()

    @staticmethod
    def delete_progress(progress_id):
        """
        Delete a progress record.

        Args:
            progress_id: ID of the progress record to delete

        Returns:
            True if deleted, False if not found
        """
        progress = Progress.query.get(progress_id)
        if progress:
            db.session.delete(progress)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_average_score(user_id):
        """
        Get the average score across all lessons for a user.

        Args:
            user_id: ID of the user

        Returns:
            Average score or None if no progress exists
        """
        from sqlalchemy import func
        result = db.session.query(
            func.avg(Progress.score).label('average')
        ).filter(
            Progress.user_id == user_id
        ).scalar()

        return float(result) if result else None