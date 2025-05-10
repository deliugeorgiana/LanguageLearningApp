from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='app/views/templates')
    app.config['SECRET_KEY'] = 'ciscosecpa55'

    # Make datetime available in all templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}

    @app.route('/')
    def index():
        return render_template('base.html')

    @app.route('/app/views/templates')
    def test_template():
        return render_template('base.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            # Add your authentication logic here
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            # Add your registration logic here
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/detail/<id>')
    def detail(id):
        return render_template('detail.html', id=id)

    @app.route('/list')
    def list():
        return render_template('list.html')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)