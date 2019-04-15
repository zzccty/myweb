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
    username = StringField('Username', validators=[
                DataRequired(), Length(2, 16), 
                regexp('^[A-Z,a-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')
                ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(1, 64)])
    image = FileField('image',validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif'], 'Images only!')])
    post_description = TextAreaField('post_description')
    body = PageDownField('body')
    tags = StringField('tags')
    categories = SelectField(u'categories', coerce=int)
    publish = SubmitField('publish')
    save = SubmitField('save')


class AddCategoryForm(FlaskForm):
    category_name = StringField('category name', validators=[DataRequired(),Length(1, 16)])
    submit = SubmitField('Add')


class Rename_CategoryForm(FlaskForm):
    old_category_name = SelectField(u'old category', coerce=int)
    new_category_name = StringField('new category name', validators=[DataRequired(),Length(1, 16)])
    submit = SubmitField('Rename')

    def validate_new_category_name(self, field):
            if Category.query.filter_by(category_name=field.data).first():
                flash("This name already exist, please try again")
                raise ValidationError('This category name already register.')

class Delete_CategoryForm(FlaskForm):
    category_name = SelectField(u'old category', coerce=int)
    submit = SubmitField('Delete')


class Delete_PostForm(FlaskForm):
    submit = SubmitField('delete')


class Edit_PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(1, 64)])
    image = FileField('image',validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif'], 'Images only!')])
    post_description = TextAreaField('post_description')
    body = PageDownField('body')
    tags = StringField('tags')
    categories = SelectField(u'categories', coerce=int)
    publish = SubmitField('publish')
    save = SubmitField('save')
