from app.models.progress import Progress
from app import db

class ProgressRepository:
    @staticmethod
    def save_progress(user_id, lesson_id, score):
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
        return Progress.query.filter_by(user_id=user_id).all()