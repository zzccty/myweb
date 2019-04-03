import os
import sys


basedir = os.path.abspath(os.path.dirname(__file__))
WIN = sys.platform.startswith('win')
if WIN:
    predix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev secret_key'