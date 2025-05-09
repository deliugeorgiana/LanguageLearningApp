from app import db
from datetime import datetime


class LearningContent(db.Model):
    """Model for educational content"""
    __tablename__ = 'learning_content'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)
    language = db.Column(db.String(10), nullable=False)
    level = db.Column(db.String(20), nullable=False)
    text_content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_featured = db.Column(db.Boolean, default=False)

    # Relationships
    vocabulary_items = db.relationship('VocabularyItem', back_populates='content', lazy=True)
    media_resources = db.relationship('MediaResource', back_populates='content', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content_type': self.content_type,
            'language': self.language,
            'level': self.level,
            'text_content': self.text_content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'author_id': self.author_id,
            'is_featured': self.is_featured
        }


class VocabularyItem(db.Model):
    """Model for vocabulary items"""
    __tablename__ = 'vocabulary_items'

    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('learning_content.id'))
    word = db.Column(db.String(100), nullable=False)
    translation = db.Column(db.String(100), nullable=False)
    part_of_speech = db.Column(db.String(20))
    example_sentence = db.Column(db.Text)
    pronunciation = db.Column(db.String(100))
    difficulty = db.Column(db.Float, default=1.0)

    # Relationships
    content = db.relationship('LearningContent', back_populates='vocabulary_items')
    user_vocabulary = db.relationship('UserVocabulary', back_populates='vocabulary_item', lazy=True)
    media_resources = db.relationship('MediaResource', back_populates='vocabulary', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'content_id': self.content_id,
            'word': self.word,
            'translation': self.translation,
            'part_of_speech': self.part_of_speech,
            'example_sentence': self.example_sentence,
            'pronunciation': self.pronunciation,
            'difficulty': self.difficulty
        }


class UserVocabulary(db.Model):
    """Model for user's personal vocabulary"""
    __tablename__ = 'user_vocabulary'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    vocabulary_id = db.Column(db.Integer, db.ForeignKey('vocabulary_items.id'))
    is_learned = db.Column(db.Boolean, default=False)
    last_practiced = db.Column(db.DateTime)
    mastery_level = db.Column(db.Float, default=0.0)
    next_review = db.Column(db.DateTime)

    # Relationships
    user = db.relationship('User', back_populates='vocabulary')
    vocabulary_item = db.relationship('VocabularyItem', back_populates='user_vocabulary')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'vocabulary_id': self.vocabulary_id,
            'is_learned': self.is_learned,
            'last_practiced': self.last_practiced.isoformat() if self.last_practiced else None,
            'mastery_level': self.mastery_level,
            'next_review': self.next_review.isoformat() if self.next_review else None
        }


class MediaResource(db.Model):
    """Model for media resources"""
    __tablename__ = 'media_resources'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))
    content_id = db.Column(db.Integer, db.ForeignKey('learning_content.id'))
    vocabulary_id = db.Column(db.Integer, db.ForeignKey('vocabulary_items.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    lesson = db.relationship('Lesson', back_populates='media_resources')
    content = db.relationship('LearningContent', back_populates='media_resources')
    vocabulary = db.relationship('VocabularyItem', back_populates='media_resources')

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'url': self.url,
            'description': self.description,
            'lesson_id': self.lesson_id,
            'content_id': self.content_id,
            'vocabulary_id': self.vocabulary_id,
            'created_at': self.created_at.isoformat()
        }