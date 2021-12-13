from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, BooleanField, SubmitField, StringField, TextAreaField, PasswordField, IntegerField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)
from .models import User

class CommentForm(FlaskForm):
    text = TextAreaField(
        "Comment", validators=[InputRequired(), Length(min=1, max=250)]
    )
    submit = SubmitField("Comment")

class PostForm(FlaskForm):
    title = StringField(validators=[InputRequired(), Length(min=1, max=50)])
    calories = IntegerField()
    text = TextAreaField(
        "Post", validators=[InputRequired(), Length(min=1, max=500)]
    )
    submit = SubmitField("Post")

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=32)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username not available")
    
    def validate_password(self, password):
        t: str = password.data
        
        if t.islower():
            raise ValidationError("Password requires at least 1 uppercase letter")
        if t.isupper():
            raise ValidationError("Password requires at least 1 lowercase letter")
        if t.isalpha():
            raise ValidationError("Password requires at least 1 numeric character")
        if t.isalnum():
            raise ValidationError("Password requires at least 1 special character")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email not available")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

class UpdateUsernameForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    submit = SubmitField("Update Username")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(username=username.data).first()
            if user is not None:
                raise ValidationError("That username is already taken")
