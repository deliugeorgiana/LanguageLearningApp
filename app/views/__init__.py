from flask import Blueprint

main_blueprint = Blueprint('main', __name__)
api_blueprint = Blueprint('api', __name__)

# Importă view-urile după ce blueprint-urile sunt definite
from . import auth_views, lesson_views