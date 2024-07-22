#!/usr/bin/python3
""" The views for the application """
import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from app import app, db, bcrypt
from app.models import Tenant, Property, Owner, TenantProperty, PropertyStatus, Rental, Messages
from .forms import RegisterForm, LoginForm, UpdateAccountForm
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


@tenant.route('/login', methods=['GET', 'POST'],)
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
            # Redirect to the previous page or to the homepage if no previous page is provided
            next_page = request.args.get('next') or url_for('main.home')
            return redirect(next_page)
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


def save_picture(form_picture):
    # Generate a random hex to prevent filename collisions
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'Tenant/static/profile_pics', picture_fn)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)
    
    # Resize the image before saving
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    # Save the picture
    i.save(picture_path)
    
    return picture_fn


@tenant.route("/account", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def accounts():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('updates.html', title='Account', image_file=image_file, form=form)


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

@tenant.route("/dashboard", methods=['GET'], strict_slashes=False)
@login_required
def dashboard():
    """Endpoint for the tenant dashboard

    Returns:
        _type_: _description_
    """
    if isinstance(current_user, Owner) or isinstance(current_user, AnonymousUserMixin):
        flash('You are not authorized to view this page', 'danger')
        return redirect(url_for('main.home'))
    # Retrieve relevant data for the tenant
    rented_properties = Property.query.join(Rental, Rental.property_id == Property.id).filter(Rental.tenant_id == current_user.id).all()
    messages = Messages.query.filter_by(receiver_id=current_user.id).all()
    return render_template('dashboard.html', rented_properties=rented_properties, messages=messages)
