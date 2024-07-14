#!/usr/bin/python3
""" The views for the application """
from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import app, db, bcrypt
from app.models import Tenant, Property, Owner, TenantProperty, PropertyStatus
from .forms import RegisterForm, LoginForm, UpdateUserAccount
from flask_login import login_user, current_user, logout_user, login_required, AnonymousUserMixin

# Declare the blueprints
tenant = Blueprint('tenant', __name__, url_prefix="/tenant", template_folder='templates', static_folder='static')

# Write the endpoints for tenants
@tenant.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():

    """Register endpoint for tenants."""
    if current_user.is_authenticated:
        flash('You are already logged in', 'info')
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        tenant = Tenant(username=form.username.data, email=form.email.data,
                        password=hashed_password, phone=form.phone.data,
                        location=form.location.data)
        db.session.add(tenant)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('tenant.login'))
    return render_template('register.html', title='Register', form=form)


@tenant.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """Login endpoint for tenants."""
    if current_user.is_authenticated:
        flash(f'You are already logged in as {current_user.username}', 'info')
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        tenant = Tenant.query.filter_by(email=form.email.data).first()
        if tenant and bcrypt.check_password_hash(tenant.password, form.password.data):
            login_user(tenant, remember=form.remember_me.data)
            flash('Login Successful', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@tenant.route('/logout')
def logout():
    """Logout endpoint for tenants."""
    logout_user()
    return redirect(url_for('tenant.login'))

@tenant.route('/dashboard')
@login_required
def dashboard():
    """Dashboard endpoint for tenants."""
    properties = Property.query.filter_by(owner_id=current_user.id).all()
    return render_template('dashboard.html', title='Dashboard', properties=properties)

@tenant.route('/account', methods=['GET', 'POST'])
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

@tenant.route('/property/<int:property_id>/apply', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def apply_property(property_id):
    """ Allows the tenant to apply for a property """
     # If the current_user is an Owner
    if isinstance(current_user, Owner):
        flash('You cannot apply for a property!', 'danger')
        return redirect(url_for("#view_property.html"))
    
    # check if the user is authenticated
    if current_user.is_authenticated or isinstance(current_user, AnonymousUserMixin):
        flash('You have to be logged in before you can apply for a property!', 'warning')
        return redirect(url_for("#home"))

    prop = Property.query.get_or_404(property_id)

    # Check if the property is already rented or sold
    if prop.property_status in [PropertyStatus.RENTED]:
        flash('Property is already Rented out', 'danger')
        return redirect(url_for("#view_property.html"))
    if prop.property_status in [PropertyStatus.SOLD]:
        flash('Property is already Sold out', 'danger')
        return redirect(url_for("#view_property.html"))

    # Check if the tenant has already applied for the property
    if prop.tenants.filter_by(id=current_user.id).first():
        flash('You have already applied for this property', 'warning')
        return redirect(url_for("#view_property.html"))
    
    # Apply for the property
    tenant_apply = TenantProperty(tenant_id=current_user.id, property_id=prop.id)
    db.session.add(tenant_apply)
    db.session.commit()
    flash('Application successful!', 'success')
    return redirect(url_for("#dashboard"))