from flask import render_template, flash, redirect, url_for, request, current_app, abort, send_from_directory
from sqlalchemy.exc import IntegrityError
from .forms import LoginForm, PostForm, AddCategoryForm, Rename_CategoryForm, Delete_CategoryForm, Delete_PostForm, Edit_PostForm
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
import os
from .. import db
from ..models import User, Tag, Post, Category
from ..utils import get_years
from . import main


@main.before_app_request
def before_request():
    pass

@main.route('/static/photos/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               filename)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('当前已登录')
        return redirect(url_for('main.index'))
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
            flash("密码或用户名错误,请重试")
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('注销成功')
    return redirect(url_for('main.index'))


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(is_draft=False).order_by(Post.timestamp.desc()).paginate(
                page, int(current_app.config['FLASKY_POSTS_PER_PAGE']), error_out=False)
    posts = pagination.items
    categories = Category.query.all()
    tags = Tag.query.all()
    return render_template('index.html', posts=posts, pagination=pagination, categories=categories, tags=tags)


@main.route('/category/<string:category_name>')
def get_posts_by_category_name(category_name):
    page = request.args.get('page', 1, type=int)
    category = Category.query.filter_by(category_name=category_name).first()
    if category is not None:
        pagination = category.posts.filter_by(is_draft=False).order_by(Post.timestamp.desc()).paginate(
                page, int(current_app.config['FLASKY_POSTS_PER_PAGE']),error_out=False)
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
        post_description = form.post_description.data
        if form.publish.data:
            f = form.image.data
            if f:
                filename = secure_filename(f.filename)
                url = os.path.join(
                    current_app.root_path, 'static', 'photos', filename
                )
                f.save(url)
                image_url = filename
            else:
                image_url = ''
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
                        tag_in.post_count += 1
                        tag_list.append(tag_in)
                    else:
                        new_tag = Tag(tag_name=tag, post_count=1)
                        db.session.add(new_tag)
                        tag_list.append(new_tag)
            post = Post(title=title, body=body, author=user, post_description=post_description,
                    category=category, tags=tag_list, years=get_years(), image_url=image_url)
        else:
            post = Post(title=title, body_draft=body, body=body, author=user, post_description=post_description, is_draft=True)
        db.session.add(post)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('发布失败')
            return redirect(url_for('main.new_post'))
        flash('发布成功')
        return redirect(url_for('main.show_post', id=post.id))
    return render_template('new_post.html', form=form)


@main.route('/post/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    user = current_user._get_current_object()
    post = Post.query.get(id)
    if post is None:
        abort(403)
    form = Edit_PostForm()
    old_cate = post.category
    old_tags = post.tags
    form.categories.choices = [(cate.id, cate.category_name) for cate in Category.query.order_by('category_name')]
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        post_description = form.post_description.data
        if form.publish.data:
            f = form.image.data
            if f:
                filename = secure_filename(f.filename)
                url = os.path.join(
                    current_app.root_path, 'static', 'photos', filename
                )
                f.save(url)
                image_url = filename
            else:
                image_url = ''
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
                        tag_in.post_count += 1
                        tag_list.append(tag_in)
                    else:
                        new_tag = Tag(tag_name=tag, post_count=1)
                        db.session.add(new_tag)
                        tag_list.append(new_tag)
            post.title = title
            post.body = body
            post.author = user
            post.post_description = post_description
            post.is_draft = False
            post.category = category
            post.tags = tag_list
            post.years = get_years()
            image_url = image_url
            if old_cate.post_count:
                old_cate.post_count -= 1
            if old_cate.post_count == 0:
                db.session.delete(cate)
            for tag in old_tags:
                if tag.post_count:
                    tag.post_count -= 1
                if tag.post_count == 0:
                    db.session.delete(tag)
        else:
            post.author = user
            post.title = title
            post.body = body
            post.body_draft = body
            post.post_description = post_description
            post.is_draft = True
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('发布失败')
            return redirect(url_for('main.new_post'))
        flash('发布成功')
        return redirect(url_for('main.show_post', id=post.id))
    
    form.title.data = post.title
    form.post_description.data = post.post_description
    if post.is_draft:
        form.body.data = post.body_draft
    else:
        form.body.data = post.body
    return render_template('edit_post.html', form=form)


@main.route('/post/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Post.query.get(id)
    if post:
        cate = post.category
        if cate.post_count:
            cate.post_count -= 1
        if cate.post_count == 0:
            db.session.delete(cate)
        for tag in post.tags:
            if tag.post_count:
                tag.post_count -= 1
            if tag.post_count == 0:
                db.session.delete(tag)
        db.session.delete(post)
        db.session.commit()
        flash("删除成功")
    else:
        flash('删除失败')
    return redirect(url_for('main.index'))


@main.route('/post/manage')
@login_required
def manage_post():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('manage_post.html', posts=posts)


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
            flash("删除成功")
            return redirect(url_for('main.index'))
        else:
            flash('删除失败')
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
            flash("分类添加成功")
            return redirect(url_for('main.index'))
        else:
            flash("分类添加失败")
            return redirect(url_for('main.manage_category'))



@main.route('/post/<int:id>')
def show_post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)


@main.route('/tag/<string:name>')
def get_post_by_tag(name):
    page = request.args.get('page', 1, type=int)
    tag = Tag.query.filter_by(tag_name=name).first_or_404()
    pagination = tag.posts.filter_by(is_draft=False).order_by(Post.timestamp.desc()).paginate(
                page, int(current_app.config['FLASKY_POSTS_PER_PAGE']),error_out=False)
    posts = pagination.items
    categories = Category.query.all()
    tags = Tag.query.all()
    return render_template('index.html', posts=posts, pagination=pagination, categories=categories, tags=tags)


@main.route('/about')
def about():
    return render_template('about.html')