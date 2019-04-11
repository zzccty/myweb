from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_moment import Moment

# import local object/module
from config import config



db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
ckeditor = CKEditor()
moment = Moment()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    ckeditor.init_app(app)
    moment.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    return app

