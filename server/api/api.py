from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_session import Session
from .config import Config
from .repositories.user_repository import UserRepository
from .repositories.fusion_repository import FusionRepository
from .repositories.preference_repository import PreferenceRepository

bcrypt = Bcrypt()
cors = CORS()
server_session = Session()

# TODO: setup CORS on frontend

def create_app(ur: UserRepository=UserRepository(), pr: PreferenceRepository=PreferenceRepository(), fr: FusionRepository=FusionRepository()):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Instantiate objects w/ current Flask Application
    bcrypt.init_app(app)
    cors.init_app(app, supports_credentials=True)
    server_session.init_app(app)   # enables server-sided sessions for flask's "session" var

    # Import route blueprints for necessary API calls
    from .auth.routes import create_blueprint as auth_bp
    app.register_blueprint(auth_bp(ur=ur, pr=pr), url_prefix='/auth')

    from .selection.routes import create_blueprint as selection_bp
    app.register_blueprint(selection_bp(fr=fr), url_prefix='/selection')

    return app

