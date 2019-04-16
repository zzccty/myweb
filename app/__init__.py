from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_moment import Moment
import os
from flask_sslify import SSLify
import logging
from logging.handlers import RotatingFileHandler

# import local object/module
from config import config


basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
sslify = SSLify()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
moment = Moment()
pagedown = PageDown()



def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)
    sslify.init_app(app)

    register_logging(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    return app

def register_logging(app):
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/love.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    if not app.debug:
        app.logger.addHandler(file_handler)