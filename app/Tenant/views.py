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

    """Register endpoint for tenants."""
    if current_user.is_authenticated:
        return redirect(url_for('tenant.dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        .decode('utf-8')
        tenant = Tenant(username=form.username.data, email=form.email.data,
                        password=hashed_password, phone=form.phone.data,
                        location=form.location.data)
        db.session.add(tenant)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('tenant.login'))
    return render_template('register.html', title='Register', form=form)


@tenant.route('/tenant/login', methods=['GET', 'POST'])
def login():
    """Login endpoint for tenants."""
    if current_user.is_authenticated:
        return redirect(url_for('tenant.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        tenant = Tenant.query.filter_by(email=form.email.data).first()
        if tenant and bcrypt.check_password_hash(tenant.password, form.password.data):
            login_user(tenant, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('tenant.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@tenant.route('/tenant/logout')
def logout():
    """Logout endpoint for tenants."""
    logout_user()
    return redirect(url_for('tenant.login'))

@tenant.route('/tenant/dashboard')
@login_required
def dashboard():
    """Dashboard endpoint for tenants."""
    properties = Property.query.filter_by(owner_id=current_user.id).all()
    return render_template('dashboard.html', title='Dashboard', properties=properties)

@tenant.route('/tenant/account', methods=['GET', 'POST'])
@login_required
def account():
    """Update account endpoint for tenants."""
    form = UpdateUserAccount()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.phone = form.phone.data
        current_user.profile_image = form.profile_image.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('tenant.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.phone.data = current_user.phone
        form.profile_image.data = current_user.profile_image
    return render_template('account.html', title='Account', form=form)