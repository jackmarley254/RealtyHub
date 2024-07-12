#!/usr/bin/python3
""" Forms for the property application """
""" Forms for the application """
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import Property



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