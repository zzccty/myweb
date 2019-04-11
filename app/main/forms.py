from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, regexp
from flask_ckeditor import CKEditorField


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
    body = CKEditorField('body')
    tags = StringField('tags')
    categories = SelectField(u'categories', coerce=int)
    submit = SubmitField('Post')