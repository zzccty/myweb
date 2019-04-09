from flask import render_template, flash, redirect, url_for, request
from .forms import LoginForm, PostForm
from flask_login import login_required, login_user, logout_user, current_user
from .. import db
from ..models import User, Tag, Post, Category
from ..utils import get_years
from . import main


@main.before_app_request
def before_request():
    pass


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash("Invalid username or password.")
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination)


@main.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    user = current_user._get_current_object()
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        tags = form.tags.data
        # 序列化tags
        tag_list = []
        if tags is not None:
            for tag in tags.split(','):
                if Tag.query.filter_by(tag_name=tag).first() is not None:
                    tag_list.append(tag)
                else:
                    db.session.add(Tag(tag_name=tag))
                    tag_list.append(tag)        
        post = Post(title=title, body=body, author=user, category=category, tags=tag_list)
        db.session.add(post)
        db.session.commit()
        flash('Post created.', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form=form)