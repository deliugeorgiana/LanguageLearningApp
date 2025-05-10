from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def init_db(app):
    """Initialize database and migrations"""
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Create tables if they don't exist
        db.create_all()

    return db