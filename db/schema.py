from datetime import datetime
from . import db


class User(db.Model):
    """User model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Relationships
    languages = db.relationship('UserLanguage', backref='user', lazy=True)
    progress = db.relationship('Progress', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class UserLanguage(db.Model):
    """Languages associated with users"""
    __tablename__ = 'user_languages'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(20), default='beginner')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<UserLanguage {self.language} ({self.level})>'


class Lesson(db.Model):
    """Lesson model"""
    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    progress = db.relationship('Progress', backref='lesson', lazy=True)

    def __repr__(self):
        return f'<Lesson {self.title} ({self.language})>'


class Progress(db.Model):
    """User progress tracking"""
    __tablename__ = 'progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    score = db.Column(db.Float, default=0)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Unique constraint
    __table_args__ = (
        db.UniqueConstraint('user_id', 'lesson_id', name='_user_lesson_uc'),
    )

    def __repr__(self):
        return f'<Progress user:{self.user_id} lesson:{self.lesson_id} score:{self.score}>'