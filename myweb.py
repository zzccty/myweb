import os
from app import create_app
from flask_migrate import Migrate


app = create_app(os.getenv('FLASK_COMFIG') or 'default')
migrate = Migrate(app)