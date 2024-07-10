#!/usr/bin/python3
""" The views for the application """
from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import app, db, bcrypt
from app.models import Messages, Property
from .forms import MessageForm
from flask_login import login_user, current_user, logout_user, login_required

# Declare the blueprints
messages = Blueprint('messages', __name__)


# Write the endpoints for messages
@messages.route('/message/send', methods=['GET', 'POST'])
def get_messd():
    pass