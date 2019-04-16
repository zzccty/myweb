from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from flask import flash
from markdown import markdown
import bleach
from . import login_manager


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(16), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

tags_posts = db.Table('tags_posts',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True)
)


# 文章描述 草稿字段
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True, index=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    body_draft = db.Column(db.Text)
    is_draft = db.Column(db.Boolean, default=False)
    topping = db.Column(db.Boolean, default=False)
    reading_volume = db.Column(db.Integer, default=0, index=True)
    post_description = db.Column(db.Text)
    image_url = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category_by_date_id = db.Column(db.Integer, db.ForeignKey('category_by_date.id'))
    category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))
    tags = db.relationship('Tag', secondary=tags_posts, lazy='subquery',
                                 backref=db.backref('posts', lazy='dynamic'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1',
                        'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'),
                                          tags=allowed_tags, strip=True))

    def __repr__(self):
        return '<Post %r>' % self.title

db.event.listen(Post.body, 'set', Post.on_changed_body)


# post count
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(16))
    post_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Tag %r>' % self.tag_name


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(64), nullable=False)
    post_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Category %r>' % self.category_name

    def delete_category(self):
        if self.id == 1:
            return False
        default_category = Category.query.get(1)
        for post in self.posts:
            post.category = default_category
            default_category.post_count += 1
        db.session.delete(self)
        db.session.commit()
        return True

    @classmethod
    def add_category(cls, category_name):
        if cls.query.filter_by(category_name=category_name).first() is not None:
            flash('这个分类已经存在，请重试')
            return False
        else:
            db.session.add(cls(category_name=category_name))
            db.session.commit()
            return True

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    url = db.Column(db.String(255))

class Category_by_date(db.Model):
    __tablename__ = "category_by_date"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    posts = db.relationship('Post', backref='years', lazy=True)

    def __repr__(self):
        return '<Category by date: %r>' % self.date

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))