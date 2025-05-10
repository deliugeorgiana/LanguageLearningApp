# app/views/__init__.py
from flask import Blueprint

# Inițializează blueprint-urile aici (fără imports circulare)
main_blueprint = Blueprint('main', __name__)
api_blueprint = Blueprint('api', __name__, url_prefix='/api')

# Importă view-urile DOAR după ce blueprint-urile sunt definite
from . import auth_views, lesson_views, progress_views