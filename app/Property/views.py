#!/usr/bin/python3
""" The views for the application """
from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import app, db, bcrypt
from app.models import User, Property
from forms import PropertyForm, UpdatePropertyForm
from flask_login import login_user, current_user, logout_user, login_required

# Declare the blueprints
proprety = Blueprint('proprety', __name__)


# Write the endpoints for properties
@proprety.route('/property/add', methods=['GET', 'POST'])
def add_property():