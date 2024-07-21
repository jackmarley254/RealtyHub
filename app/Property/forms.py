#!/usr/bin/python3
""" Forms for the property application """
""" Forms for the application """
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,DateField, IntegerField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange, Optional
from flask_wtf.file import FileAllowed
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
    bedrooms = IntegerField('Nos Bedrooms', validators=[DataRequired(), NumberRange(min=1)])
    bathrooms = IntegerField('Nos Bathrooms', validators=[DataRequired(), NumberRange(min=1)])
    size = IntegerField('Size (sq ft)', validators=[DataRequired(), NumberRange(min=0)])
    available_from = DateField('Available From', format='%Y-%m-%d', validators=[DataRequired()])
    image1 = FileField('Image 1', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    image2 = FileField('Image 2', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    image3 = FileField('Image 3', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Create Property')

class UpdatePropertyForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    property_type = SelectField('Property Type', choices=[('House', 'House'), ('Apartment', 'Apartment'), ('Condo', 'Condo')], validators=[DataRequired()])
    property_status = SelectField('Property Status', choices=[('For Sale', 'For Sale'), ('For Rent', 'For Rent')], validators=[DataRequired()])
    bedrooms = IntegerField('Bedrooms', validators=[DataRequired()])
    bathrooms = IntegerField('Bathrooms', validators=[DataRequired()])
    size = IntegerField('Size (sqft)', validators=[DataRequired()])
    # amenities = StringField('Amenities')
    available_from = DateField('Available From', format='%Y-%m-%d')
    thumbnail1 = FileField('Thumbnail 1')
    thumbnail2 = FileField('Thumbnail 2')
    thumbnail3 = FileField('Thumbnail 3')
    submit = SubmitField('Update')


class SearchForm(FlaskForm):
    """ The search form

    Args:
        FlaskForm (_type_): _description_
    """
    location = StringField('Location', validators=[Optional()])
    min_price = IntegerField('Min Price $', validators=[Optional(), NumberRange(min=0)])
    max_price = IntegerField('Max Price $', validators=[Optional(), NumberRange(min=0)])
    property_type = SelectField('Property Type', choices=[('House', 'House'), ('Apartment', 'Apartment')], validators=[DataRequired()])
    property_status = SelectField('Property Status', choices=[('For Sale', 'For Sale'), ('For Rent', 'For Rent')], validators=[DataRequired()])
    min_bedrooms = IntegerField('Min Bedrooms', validators=[Optional(), NumberRange(min=0)])
    min_bathrooms = IntegerField('Min Bathrooms', validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField('Search')