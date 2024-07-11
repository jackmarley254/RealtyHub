#!/usr/bin/python3
""" we will use here for urls for the homepage"""
from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import app, db, bcrypt
from app.models import Tenant, Property
from flask_login import login_user, current_user, logout_user, login_required

# Declare the blueprints
main = Blueprint('main', __name__, url_prefix="/main", template_folder='templates', static_folder='static')


@main.route('/', methods=['GET', 'POST'], strict_slashes=False)
def home():
    """ homepage """
    return render_template('layout.html')