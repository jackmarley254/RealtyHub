#!/usr/bin/python3
""" The views for the application """
import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, Blueprint, abort, current_app
from app import app, db, bcrypt
from app.models import Messages, Property, Owner, Messages, Tenant
from .forms import RegisterForm, LoginForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required, AnonymousUserMixin

# Declare the blueprints
owner = Blueprint('owner', __name__, url_prefix="/owner", template_folder='templates', static_folder='static')



# Write the endpoints for owners
@owner.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    if current_user.is_authenticated:
        flash('You are already logged in', 'info')
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Owner(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            location=form.location.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('owner.login'))
    return render_template('registers.html', title='Register', form=form)


@owner.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Owner.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.
                                               password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Login successful', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            
            flash('Login unsuccesful. Please check email and password', 'danger')
    return render_template('logins.html', title='Login', form=form)


def save_picture(form_picture):
    # Generate a random hex to prevent filename collisions
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, '/Owner/static/profile_pics', picture_fn)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)
    
    # Resize the image before saving
    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    # Save the picture
    i.save(picture_path)
    
    return picture_fn

@owner.route("/account", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('owner.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    
    return render_template('update.html', title='Account', image_file=image_file, form=form)


@owner.route("/dashboard", methods=['GET'])
@login_required
def dashboard():
    """ routes to the dasboard

    Returns:
        _type_: _description_
    """
    if not current_user.is_authenticated or isinstance(current_user, AnonymousUserMixin):
        flash('You do not have permission to view this page', 'danger')
        return redirect(url_for('main.home'))
    # Retrieve relevant data for the owner
    properties = Property.query.filter_by(owner_id=current_user.id).all()
    messages = Messages.query.filter_by(receiver_id=current_user.id).all()
    # tenants = Tenant.query.filter(Property.owner_id==current_user.id).all()
    return render_template('on_dasboard.html', properties=properties, messages=messages)



@owner.route('/properties', methods=['GET'])
def view_properties():
    properties = Property.query.all()
    return render_template('view_properties.html', properties=properties)


@owner.route('/property/<int:property_id>', methods=['GET'])
def view_property(property_id):
    propertys = Property.query.get_or_404(property_id)
    return render_template('view_property.html', property=propertys)


@owner.route('/owner/property/<int:property_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_property(property_id):
    property = Property.query.get_or_404(property_id)
    if property.owner_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        property.title = request.form['title']
        property.description = request.form['description']
        property.price = request.form['price']
        property.location = request.form['location']
        property.property_type = request.form['property_type']
        property.bedrooms = request.form['bedrooms']
        property.bathrooms = request.form['bathrooms']
        property.size = request.form['size']
        # property.amenities = request.form['amenities']
        property.available_from = request.form['available_from']

        db.session.commit()
        flash('Your property has been updated', 'success')
        return redirect(url_for('owner.view_property', property_id=property
                                .id))

    return render_template('edit_property.html', title='Edit Property',
                           property=property)


@owner.route('/owner/property/<int:property_id>/delete', methods=['POST'])
@login_required
def delete_property(property_id):
    property = Property.query.get_or_404(property_id)
    if property.owner_id != current_user.id:
        abort(403)
    db.session.delete(property)
    db.session.commit()
    flash('Your property has been deleted!', 'success')
    return redirect(url_for('owner.view_properties'))


@owner.route('/messages', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def messages():
    messages = Messages.query.filter_by(receiver_id=current_user.id).all()
    return render_template('#messages.html', messages=messages)