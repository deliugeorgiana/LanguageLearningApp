from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initializează extensii
    db.init_app(app)
    migrate.init_app(app, db)

    # Înregistrează blueprint-uri
    from app.api.auth_routes import auth_bp
    from app.api.lesson_routes import lesson_bp
    from app.api.progress_routes import progress_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(lesson_bp, url_prefix='/api/lessons')
    app.register_blueprint(progress_bp, url_prefix='/api/progress')

    # Ruta principală
    @app.route('/')
    def index():
        return jsonify({
            "message": "Language Learning API",
            "endpoints": {
                "auth": "/api/auth/",
                "lessons": "/api/lessons/",
                "progress": "/api/progress/"
            }
        })

    return app