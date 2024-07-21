#!/usr/bin/env python3
""" The message form"""
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired
from app.models import Messages


class MessageForm(FlaskForm):
    """ The message form

    Args:
        FlaskForm (_type_): The message form to validate the message
    """
    recipient = StringField('Recipient', validators=[DataRequired()])
    content = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')
    
class ReplyForm(FlaskForm):
    message = TextAreaField('Reply', validators=[DataRequired()])
    submit = SubmitField('Send Reply')