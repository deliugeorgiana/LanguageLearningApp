from app import db
from datetime import datetime


class Lesson(db.Model):
    """Model for lessons"""
    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    progress_entries = db.relationship('Progress', back_populates='lesson', lazy=True)
    media_resources = db.relationship('MediaResource', back_populates='lesson', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'language': self.language,
            'difficulty': self.difficulty,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }