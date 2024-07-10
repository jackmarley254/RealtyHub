#!/usr/bin/python3
""" The views for the application """
from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import app, db, bcrypt
from app.models import Tenant, Property
from .forms import RegisterForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

# Declare the blueprints
tenant = Blueprint('tenant', __name__)

# Write the endpoints for tenants
@tenant.route('/tenant/register', methods=['GET', 'POST'])
def register():
    pass