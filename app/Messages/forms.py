#!/usr/bin/env python3
""" The message form"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from app.models import Messages


class MessageForm(FlaskForm):
    """ The message form

    Args:
        FlaskForm (_type_): Message form to validate the message
    """
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')
