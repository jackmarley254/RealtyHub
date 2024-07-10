#!/usr/bin/python3
""" The views for the application """
from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.models import User, Property
from forms import RegisterForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

# Declare the blueprints
owner = Blueprint('owner', __name__)


# Write the endpoints for owners
@owner.route('/owner/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        .decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
                    password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('owner.login'))
    return render_template('register.html', title='Register', form=form)


@owner.route('/owner/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.
                                               password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect
        (url_for('main.home'))
        else:
            flash('Login unsuccesful. Please check email and
                  password', 'danger')
    return render_template('login.html', title='Login', form=form)


@owner.route('/owner/property/new', methods=['GET', 'POST'])
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
