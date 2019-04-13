from flask import render_template, flash, redirect, url_for, request, current_app
from sqlalchemy.exc import IntegrityError
from .forms import LoginForm, PostForm, AddCategoryForm, Rename_CategoryForm, Delete_CategoryForm
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
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        else:
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
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
                page, current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    posts = pagination.items
    categories = Category.query.all()
    tags = Tag.query.all()
    return render_template('index.html', posts=posts, pagination=pagination, categories=categories, tags=tags)


@main.route('/category/<string:category_name>')
def get_posts_by_category_name(category_name):
    page = request.args.get('page', 1, type=int)
    category = Category.query.filter_by(category_name=category_name).first()
    if category is not None:
        pagination = category.posts.order_by(Post.timestamp.desc()).paginate(
                page, current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
        posts = pagination.items
        categories = Category.query.all()
        tags = Tag.query.all()
        return render_template('index.html', posts=posts, pagination=pagination, categories=categories, tags=tags)



@main.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    user = current_user._get_current_object()
    form = PostForm()
    form.categories.choices = [(cate.id, cate.category_name) for cate in Category.query.order_by('category_name')]
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        description = form.description.data
        category = Category.query.get(form.categories.data)
        if category is not None:
            category.post_count += 1
        tags = form.tags.data
        # 序列化tags
        tag_list = []
        if tags is not None:
            for tag in tags.split(','):
                tag_in = Tag.query.filter_by(tag_name=tag).first() 
                if tag_in:
                    tag_list.append(tag_in)
                else:
                    new_tag = Tag(tag_name=tag)
                    db.session.add(new_tag)
                    tag_list.append(new_tag)    
        post = Post(title=title, body=body, author=user, description=description,
                    category=category, tags=tag_list, years=get_years())
        db.session.add(post)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollBack()
            flash('Post Failed')
            return redirect(url_for('main.new_post'))
        flash('Post created success')
        return redirect(url_for('main.show_post', id=post.id))
    return render_template('new_post.html', form=form)


@main.route('/category/manage')
@login_required
def manage_category():
    add_category_form = AddCategoryForm()
    rename_category_form = Rename_CategoryForm()
    delete_category_form = Delete_CategoryForm()
    choices = [(cate.id, cate.category_name) for cate in Category.query.order_by('category_name')]
    rename_category_form.old_category_name.choices = choices
    delete_category_form.category_name.choices = choices

    return render_template('manage_cate.html', 
                            add_category_form=add_category_form, 
                            rename_category_form=rename_category_form,
                            delete_category_form=delete_category_form)


@main.route('/category/delete', methods=['POST'])
@login_required
def delete_category():
    delete_category_form = Delete_CategoryForm()
    delete_category_form.category_name.choices = [(cate.id, cate.category_name) for cate in Category.query.order_by('category_name')]
    if delete_category_form.validate_on_submit():
        category = Category.query.get(delete_category_form.category_name.data)
        if category.delete_category():
            flash("Delete success.")
            return redirect(url_for('main.index'))
        else:
            flash('Failed to delete category')
            return redirect(url_for('main.manage_category'))


@main.route('/category/rename', methods=['POST'])
@login_required
def rename_category():
    rename_category_form = Rename_CategoryForm()
    rename_category_form.old_category_name.choices = [(cate.id, cate.category_name) for cate in Category.query.order_by('category_name')]
    if rename_category_form.validate_on_submit():
        category = Category.query.get(rename_category_form.old_category_name.data)
        category.category_name = rename_category_form.new_category_name.data
        db.session.commit()
        return redirect(url_for('main.index'))
    return redirect(url_for('main.manage_category'))



@main.route('/category/add', methods=['POST'])
@login_required
def add_category():
    add_category_form = AddCategoryForm()
    if add_category_form.validate_on_submit():
        category_name = add_category_form.category_name.data
        if Category.add_category(category_name):
            flash("Add category success.")
            return redirect(url_for('main.index'))
        else:
            flash('Failed to add category')
            return redirect(url_for('main.manage_category'))



@main.route('/post/<int:id>')
def show_post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)


@main.route('/tag/<string:name>')
def get_post_by_tag(name):
    page = request.args.get('page', 1, type=int)
    tag = Tag.query.filter_by(tag_name=name).first_or_404()
    pagination = tag.posts.order_by(Post.timestamp.desc()).paginate(
                page, current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    posts = pagination.items
    categories = Category.query.all()
    tags = Tag.query.all()
    return render_template('index.html', posts=posts, pagination=pagination, categories=categories, tags=tags)


@main.route('/test_login')
@login_required
def test_login():
    return r'Test success!'