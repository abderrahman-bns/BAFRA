from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from faceApp.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    profile = HiddenField('profil')
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class ResetForm(FlaskForm):
    old_password = PasswordField('Your Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Reset Password')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    nom = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    prenom = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    age = IntegerField('Age', validators=[DataRequired()])
    sex = StringField('Sex', validators=[DataRequired(), Length(max=1)])
    tel = StringField('Tel', validators=[DataRequired(), Length(10)])
    profile = StringField('Profil')
    departement = StringField('Departement', validators=[DataRequired()])
    fonction = StringField('Fonction', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    video_file = StringField('Video')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):

        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class ContactForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired("Please enter your name."), Length(max=20)])
  email = StringField("Email", validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
  subject = StringField("Subject", validators=[DataRequired("Please enter a subject.")])
  message = TextAreaField("Message", validators=[DataRequired("Please enter a message.")])
  submit = SubmitField("Send your message!")