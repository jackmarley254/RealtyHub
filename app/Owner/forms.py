#!/usr/bin/python3
""" Forms for the application """
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_wtf.file import FileAllowed
from app.models import Owner


class RegisterForm(FlaskForm):
    """ The registration form """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    location = StringField('Location', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')
    
    # Custom validation to check if the email already exists
    def validate_email(self, email):
        """ Querys the database to check if the email already exists

        Args:
            email (_type_): The email to be validated

        Raises:
            ValidationError: Raises a validation error if the email already exists
        """
        user_email = Owner.query.filter_by(email=email.data).first()
        if user_email:
            raise ValidationError('Email already exists. Please use a different email address')


    # Custom validation to check if the username already exists
    def validate_username(self, username):
        """ Querys the database to check if the username already exists

        Args:
            username (_type_): The username to be validated

        Raises:
            ValidationError: Raises a validation error if the username already exists
        """
        user_name = Owner.query.filter_by(username=username.data).first()
        if user_name:
            raise ValidationError('Username already exists. Please use a different username')

class LoginForm(FlaskForm):
    """ The login form

    Args:
        FlaskForm (_type_): Login form to validate the user
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """ Update account form

    Args:
        FlaskForm (_type_): _description_

    Raises:
        ValidationError: _description_
        ValidationError: _description_
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Owner.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Owner.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
