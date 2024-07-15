#!/usr/bin/python3
""" The views for the application """
from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from app import app, db, bcrypt
from app.models import Messages, Property, Owner
from .forms import RegisterForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

# Declare the blueprints
owner = Blueprint('owner', __name__, url_prefix="/investor", template_folder='templates', static_folder='static')

@owner.route('/', methods=['GET', 'POST'], strict_slashes=False)
def owner_home():
    return render_template('layout.html')


# Write the endpoints for owners
@owner.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    if current_user.is_authenticated:
        flash('You are already logged in', 'info')
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        owner = Owner(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            location=form.location.data,
            password=hashed_password
        )
        db.session.add(owner)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('owner.login'))
    return render_template('register.html', title='Register', form=form)


@owner.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        owner = Owner.query.filter_by(email=form.email.data).first()
        if owner and bcrypt.check_password_hash(owner.password, form.
                                               password.data):
            login_user(owner, remember=form.remember_me.data)
            flash('Login successful', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            
            flash('Login unsuccesful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@owner.route('/new', methods=['GET', 'POST'])
@login_required
def new_property():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        location = request.form['location']
        property_type = request.form['property_type']
        bedrooms = request.form['bedrooms']
        bathrooms = request.form['bathrooms']
        size = request.form['size']
        # amenities = request.form['amenities']
        available_from = request.form['available_from']

        new_property = Property(
            title=title,
            description=description,
            price=price,
            location=location,
            property_type=property_type,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            size=size,
            # amenities=amenities,
            available_from=available_from,
            owner_id=current_user.id
        )

        db.session.add(new_property)
        db.session.commit()
        flash('Your property has been created!', 'success')
        return redirect(url_for('owner.view_properties'))

    return render_template('create_property.html', title='New Property')


@owner.route('/properties', methods=['GET'])
def view_properties():
    properties = Property.query.all()
    return render_template('view_properties.html', properties=properties)


@owner.route('/property/<int:property_id>', methods=['GET'])
def view_property(property_id):
    property = Property.query.get_or_404(property_id)
    return render_template('view_property.html', property=property)


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
