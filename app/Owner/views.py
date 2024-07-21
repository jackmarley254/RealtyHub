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
           # Redirect to the previous page or to the homepage if no previous page is provided
            next_page = request.args.get('next') or url_for('main.home')
            return redirect(next_page)
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


