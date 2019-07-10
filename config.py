import os
import sys


basedir = os.path.abspath(os.path.dirname(__file__))
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or False
    FLASKY_POSTS_PER_PAGE = os.environ.get('FLASKY_POSTS_PER_PAGE') or 20
    FLASK_ADMIN_NAME = os.environ.get('FLASK_ADMIN_NAME') or 'test'
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'static/photos'


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCJEMY_DATABASE_URI') or prefix + os.path.join(basedir, 'data.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))

config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
