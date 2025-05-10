from . import db
from .schema import User, UserLanguage, Lesson, Progress
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta


def seed_database():
    """Seed the database with initial data"""

    # Clear existing data
    db.session.query(Progress).delete()
    db.session.query(Lesson).delete()
    db.session.query(UserLanguage).delete()
    db.session.query(User).delete()
    db.session.commit()

    # Create test users
    users = [
        User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            is_active=True
        ),
        User(
            username='student',
            email='student@example.com',
            password_hash=generate_password_hash('student123'),
            is_active=True
        )
    ]
    db.session.bulk_save_objects(users)
    db.session.commit()

    # Add user languages
    languages = [
        UserLanguage(user_id=1, language='english', level='advanced'),
        UserLanguage(user_id=1, language='french', level='intermediate'),
        UserLanguage(user_id=2, language='english', level='beginner')
    ]
    db.session.bulk_save_objects(languages)
    db.session.commit()

    # Create lessons
    lessons = [
        Lesson(
            title='English Basics',
            content='Introduction to English grammar...',
            language='english',
            difficulty='beginner'
        ),
        Lesson(
            title='Intermediate French',
            content='French verb conjugations...',
            language='french',
            difficulty='intermediate'
        ),
        Lesson(
            title='Advanced English Writing',
            content='Academic writing techniques...',
            language='english',
            difficulty='advanced'
        )
    ]
    db.session.bulk_save_objects(lessons)
    db.session.commit()

    # Create progress records
    progress = [
        Progress(
            user_id=2,
            lesson_id=1,
            score=85.5,
            completed=True,
            completed_at=datetime.utcnow() - timedelta(days=2)
        ),
        Progress(
            user_id=1,
            lesson_id=3,
            score=92.0,
            completed=True,
            completed_at=datetime.utcnow() - timedelta(days=5)
        )
    ]
    db.session.bulk_save_objects(progress)
    db.session.commit()

    print("Database seeded successfully!")