#!/usr/bin/python3
""" Forms for the application """
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User, Property
from flask_login import current_user


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
        user_email = User.query.filter_by(email=email.data).first()
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
        user_name = User.query.filter_by(username=username.data).first()
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


class UpdateUserAccount(FlaskForm):
    """ The update user account form

    Args:
        FlaskForm (_type_): Update user account form to validate the user
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    profile_image = StringField('Profile Image')
    submit = SubmitField('Update')


class PropertyForm(FlaskForm):
    """ The property form

    Args:
        FlaskForm (_type_): Property form to validate the property
    """
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    property_type = StringField('Property Type', validators=[DataRequired()])
    property_status = StringField('Property Status', validators=[DataRequired()])
    bathrooms = StringField('Bathrooms', validators=[DataRequired()])
    bedrooms = StringField('Bedrooms', validators=[DataRequired()])
    size = StringField('Size', validators=[DataRequired()])
    submit = SubmitField('Create Property')


class UpdatePropertyForm(FlaskForm):
    """ The update property form

    Args:
        FlaskForm (_type_): Update property form to validate the property
    """
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    property_type = StringField('Property Type', validators=[DataRequired()])
    property_status = StringField('Property Status', validators=[DataRequired()])
    bathrooms = StringField('Bathrooms', validators=[DataRequired()])
    bedrooms = StringField('Bedrooms', validators=[DataRequired()])
    size = StringField('Size', validators=[DataRequired()])
    submit = SubmitField('Update Property')
    
    # Validate the property owner
    def validate_property_owner(self, owner_id):
        """ Validate the property owner, to make sure only the owner can update the property

        Args:
            owner_id (_type_): The owner id to be validated
        """
        # we have to query the database to get the owner id
        property_owner = Property.query.filter_by(owner_id=owner_id).first()
        if current_user.id != property_owner.owner_id:
            raise ValidationError('You are not the owner of this property')


class MessageForm(FlaskForm):
    """ The message form

    Args:
        FlaskForm (_type_): Message form to validate the message
    """
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')
