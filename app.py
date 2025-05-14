from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    profile = db.relationship('UserProfile', backref='user', uselist=False)

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    language = db.Column(db.String(50), default='engleză')
    level = db.Column(db.String(50), default='începător')
    completed_lessons = db.Column(db.Integer, default=0)
    total_score = db.Column(db.Integer, default=0)
    total_time = db.Column(db.Integer, default=0)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# App factory
def create_app():
    app = Flask(__name__, template_folder='app/views/templates')
    app = Flask(__name__, static_folder='static', template_folder='app/views/templates')

    app.config['SECRET_KEY'] = 'ciscosecpa55'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}

    @app.route('/')
    def home_redirect():
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Login failed. Please try again.', 'danger')
        return render_template('auth/login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
            if existing_user:
                flash('User already exists!', 'danger')
                return redirect(url_for('register'))
            hashed_pw = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()

            profile = UserProfile(user_id=new_user.id)
            db.session.add(profile)
            db.session.commit()

            login_user(new_user)
            flash('Registration successful!', 'success')
            return redirect(url_for('dashboard'))
        return render_template('auth/register.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        profile = current_user.profile
        if request.method == 'POST':
            profile.language = request.form['language']
            profile.level = request.form['level']
            db.session.commit()
            flash('Profil actualizat cu succes!', 'success')
            return redirect(url_for('profile'))
        return render_template('profile.html', profile=profile)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Logged out successfully.', 'info')
        return redirect(url_for('login'))
    
    @app.route('/lessons')
    @login_required
    def lessons():
        return render_template('lessons.html')


    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
