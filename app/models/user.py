from werkzeug.security import check_password_hash
from app import db
from datetime import datetime
from typing import List
from app.utils.security import generate_password_hash


class UserLanguage(db.Model):
    """Model for tracking user's language proficiency"""
    __tablename__ = 'user_languages'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    language = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(20), default='beginner')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='languages')

    def to_dict(self):
        return {
            'id': self.id,
            'language': self.language,
            'level': self.level,
            'created_at': self.created_at.isoformat()
        }


class User(db.Model):
    """Main user model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Relationships
    languages = db.relationship('UserLanguage', back_populates='user', lazy=True, cascade='all, delete-orphan')
    progress = db.relationship('Progress', back_populates='user', lazy=True)
    vocabulary = db.relationship('UserVocabulary', back_populates='user', lazy=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }