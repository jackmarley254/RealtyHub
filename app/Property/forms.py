#!/usr/bin/python3
""" Forms for the property application """
""" Forms for the application """
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,DateField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from app.models import Property



class PropertyForm(FlaskForm):
    """ The property form

    Args:
        FlaskForm (_type_): Property form to validate the property
    """
    title = StringField('Title', validators=[DataRequired(), Length(min=4, max=200)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=0)])
    location = StringField('Location', validators=[DataRequired(), Length(min=2, max=200)])
    property_type = SelectField('Property Type', choices=[('House', 'House'), ('Apartment', 'Apartment'), ('Condo', 'Condo')], validators=[DataRequired()])
    property_status = SelectField('Property Status', choices=[('For Sale', 'For Sale'), ('For Rent', 'For Rent')], validators=[DataRequired()])
    bedrooms = IntegerField('Bedrooms', validators=[DataRequired(), NumberRange(min=1)])
    bathrooms = IntegerField('Bathrooms', validators=[DataRequired(), NumberRange(min=1)])
    size = IntegerField('Size (sq ft)', validators=[DataRequired(), NumberRange(min=0)])
    available_from = DateField('Available From', format='%Y-%m-%d', validators=[DataRequired()])
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