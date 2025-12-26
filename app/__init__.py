from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap5
from flask_gravatar import Gravatar

from config import config
from .base import Base

# ---------------
db = SQLAlchemy(model_class=Base)
ckeditor = CKEditor()
bootstrap = Bootstrap5()
gravatar = Gravatar()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message= "Please log in to view your own profile page!"
login_manager.login_message_category = "primary"

# ---------------
# Because it is defined in the app/__init__.py, any 'from app import' can only import anything inside __init__
def create_app(config_name = "default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    gravatar.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .user import user as user_profile_blueprint
    app.register_blueprint(user_profile_blueprint)

    return app
