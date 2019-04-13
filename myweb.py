import os
from app import create_app, db
from flask_migrate import Migrate
from app.models import User, Tag, Category, Post, Category_by_date


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Tag=Tag, Category=Category, Post=Post, Category_by_date=Category_by_date)