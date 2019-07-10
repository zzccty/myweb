from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, regexp
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from flask_pagedown.fields import PageDownField
from ..models import Category
from wtforms import ValidationError
from flask import flash


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[
                DataRequired(), Length(2, 16),
                regexp('^[A-Z,a-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')
                ])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登入')


class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 64)])
    image = FileField('文章插图', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif'], 'Images only!')])
    post_description = TextAreaField('文章描述')
    body = PageDownField('内容')
    tags = StringField('标签')
    categories = SelectField(u'选择分类', coerce=int)
    publish = SubmitField('发布')
    save = SubmitField('存为草稿')


class AddCategoryForm(FlaskForm):
    category_name = StringField('分类名称', validators=[DataRequired(), Length(1, 16)])
    submit = SubmitField('增加')


class Rename_CategoryForm(FlaskForm):
    old_category_name = SelectField(u'旧分类', coerce=int)
    new_category_name = StringField('新分类', validators=[DataRequired(), Length(1, 16)])
    submit = SubmitField('重命名')

    def validate_new_category_name(self, field):
            if Category.query.filter_by(category_name=field.data).first():
                flash("用户名已经存在，请重试")
                raise ValidationError('这个分类名称已被注册')


class Delete_CategoryForm(FlaskForm):
    category_name = SelectField(u'选择分类', coerce=int)
    submit = SubmitField('删除')


class Delete_PostForm(FlaskForm):
    submit = SubmitField('删除')


class Edit_PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 64)])
    image = FileField('文章插图', validators=[FileAllowed(['jpg', 'png', 'gif'], 'Images only!')])
    post_description = TextAreaField('文章描述')
    body = PageDownField('内容')
    tags = StringField('标签')
    categories = SelectField(u'选择分类', coerce=int)
    publish = SubmitField('发布')
    save = SubmitField('存为草稿')
