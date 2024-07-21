#!/usr/bin/python3
""" The views for the application """
import os
from werkzeug.utils import secure_filename
import secrets
from flask import render_template, url_for, flash, redirect, request, Blueprint, abort, current_app
from app import app, db
from datetime import datetime
from PIL import Image
from app.models import Owner, Property, Tenant, PropertyStatus, TenantProperty
from .forms import PropertyForm, UpdatePropertyForm, SearchForm
from flask_login import current_user, login_required, AnonymousUserMixin

# Declare the blueprints
proprety = Blueprint('proprety', __name__, url_prefix="/property", template_folder='templates', static_folder='static')



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/property_pics', picture_fn)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)

    # Save the original picture
    form_picture.save(picture_path)

    # Create and save a thumbnail
    thumbnail_size = (300, 300)
    thumbnail_fn = random_hex + '_thumb' + f_ext
    thumbnail_path = os.path.join(current_app.root_path, 'static/property_pics', thumbnail_fn)

    i = Image.open(form_picture)
    i.thumbnail(thumbnail_size)
    i.save(thumbnail_path)

    return picture_fn, thumbnail_fn


@proprety.route('/add_new', methods=['GET', 'POST'], strict_slashes=False)
def create_property():
    """ Allows the owner to add a property """
    # Checking if the current user is authenticated
    if not current_user.is_authenticated or isinstance(current_user, AnonymousUserMixin):
        flash('You have to be logged in before you can post a property!', 'warning')
        return redirect(url_for("main.home"))
    
    # We check if the current_user is a Tenant
    if isinstance(current_user, Tenant):
        flash('You cannot create a property!', 'danger')
        return redirect(url_for("main.home"))
    
    # if the current_user is an Owner
    form = PropertyForm()
    if form.validate_on_submit():
        new_property = Property(
            title=form.title.data,
            description=form.description.data,
            price=int(form.price.data),
            location=form.location.data,
            property_type=form.property_type.data,
            property_status=form.property_status.data,
            bedrooms=int(form.bedrooms.data),
            bathrooms=int(form.bathrooms.data),
            size=int(form.size.data),
            available_from=datetime.strptime(str(form.available_from.data), '%Y-%m-%d'),
            owner_id=current_user.id
        )

        # Handle image uploads
        if form.image1.data:
            image1, thumbnail1 = save_picture(form.image1.data)
            new_property.image1 = image1
            new_property.thumbnail1 = thumbnail1
        if form.image2.data:
            image2, thumbnail2 = save_picture(form.image2.data)
            new_property.image2 = image2
            new_property.thumbnail2 = thumbnail2
        if form.image3.data:
            image3, thumbnail3 = save_picture(form.image3.data)
            new_property.image3 = image3
            new_property.thumbnail3 = thumbnail3

        try:
            db.session.add(new_property)
            db.session.commit()
            flash('Property posted successfully', 'success')
            return redirect(url_for('main.home'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error posting property: {str(e)}', 'danger')
    
    return render_template('create_property.html', form=form)


@proprety.route('/<int:property_id>/update', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def update_property(property_id):
    """ Allows the owner to update a property """
    # we check if the current_user is an Owner
    prop = Property.query.get_or_404(id=property_id)
    if prop.owners != current_user.id:
        abort(403)
    
    form = UpdatePropertyForm()
    if  form.validate_on_submit():  
        prop.title = request.form.get('title')
        prop.description = request.form.get('description')
        prop.price = request.form.get('price')
        prop.location = request.form.get('location')
        prop.property_type = request.form.get('property_type')
        prop.bedrooms = request.form.get('bedrooms')
        prop.bathrooms = request.form.get('bathrooms')
        prop.size = request.form.get('size')
        prop.amenities = request.form.get('amenities')
        prop.available_from = request.form.get('available_from')

        db.session.commit()
        flash('Property updated successfully', 'success')
    elif request.method == 'GET':
        form.title.data = prop.title
        form.description.data = prop.description
        form.price.data = prop.price
        form.location.data = prop.location
        form.property_type.data = prop.property_type
        form.bedrooms.data = prop.bedrooms
        form.bathrooms.data = prop.bathrooms
        form.size.data = prop.size
        form.amenities.data = prop.amenities
        form.available_from.data = prop.available_from

    return render_template('#update_property.html', form=form)

@proprety.route('properties/<int:property_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_property(property_id):
    """ Allows the owner to delete a property """
    # Query the database to get the property
    prop = Property.query.get_or_404(property_id)
    if prop.owners != current_user.id:
        abort(403)

    db.session.delete(prop)
    db.session.commit()
    flash('Property deleted successfully', 'success')


@proprety.route('properties/<int:property_id>/view', methods=['GET'])
def view_property(property_id):
    """ Allows the tenant to view a property """
    prop = Property.query.get_or_404(property_id)
    return render_template('view_property.html', title=prop.title, property=prop)

    
@proprety.route('/search', methods=['GET', 'POST'], strict_slashes=False)
def search_properties():
    form = SearchForm()
    properties_list = []
    if form.validate_on_submit():
        location = form.location.data
        min_price = form.min_price.data
        max_price = form.max_price.data
        property_type = form.property_type.data
        property_status = form.property_status.data
        min_bedrooms = form.min_bedrooms.data
        min_bathrooms = form.min_bathrooms.data

        limit = 10
        offset = 0

        query = Property.query

        if location:
            query = query.filter(Property.location.ilike(f"%{location}%"))
        if min_price is not None:
            query = query.filter(Property.price >= min_price)
        if max_price is not None:
            query = query.filter(Property.price <= max_price)
        if property_type:
            query = query.filter(Property.property_type == property_type)
        if property_status:
            query = query.filter(Property.property_status == property_status)
        if min_bedrooms is not None:
            query = query.filter(Property.bedrooms >= min_bedrooms)
        if min_bathrooms is not None:
            query = query.filter(Property.bathrooms >= min_bathrooms)

        properties = query.limit(limit).offset(offset).all()
        properties_list = [
            {
                'id': property_item.id,
                'title': property_item.title,
                'description': property_item.description,
                'price': property_item.price,
                'location': property_item.location,
                'property_type': property_item.property_type,
                'property_status': property_item.property_status,
                'bedrooms': property_item.bedrooms,
                'bathrooms': property_item.bathrooms,
                'size': property_item.size,
                'available_from': property_item.available_from,
                'owner_id': property_item.owner_id,
                'created_at': property_item.created_at,
                'thumbnail1': property_item.thumbnail1
            }
            for property_item in properties
        ]
         # Debugging individual property attributes
        # for prop in properties_list:
            # print("Data:", prop) 
            # print("Thumbnail path:", prop.get('thumbnail1'))

        if not properties_list:
            flash('No properties found matching the search criteria.', 'warning')

    return render_template('search.html', form=form, properties=properties_list)

 
@proprety.route('/properties', methods=['GET'], strict_slashes=False)
def get_properties():
    """ Get all properties """
    # Pagination settings
    page = request.args.get('page', 1, type=int)
    per_page = 9  # 3 columns * 3 rows

    properties = Property.query.paginate(page=page, per_page=per_page)
    
    return render_template('show_property.html', properties=properties.items, pagination=properties)

@login_required
def view_created_property():
    """ Allows the owner view created properties """
    # if the current_user is a Tenant
    if isinstance(current_user, Tenant):
        abort(403)
    user_id = current_user.id
    user = Owner.query.get_or_404(user_id)
    
    # Get all the properties owned by the user
    user_properties = Property.query.filter_by(owner_id=user.id).all()
    
    return render_template('dashboard.html', user=user, properties=user_properties)
