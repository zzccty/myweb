import os
from app import create_app, db
from flask_migrate import Migrate
from app.models import User, Tag, Category, Post, Category_by_date
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.getenv('FLASK_CONFIG') or 'production')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Tag=Tag, Category=Category, Post=Post, Category_by_date=Category_by_date)