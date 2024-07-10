#!/usr/bin/python3
""" The views for the application """
from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify, abort
from app import app, db, bcrypt
from app.models import Owner, Property, Tenant, PropertyStatus, TenantProperty
from forms import PropertyForm, UpdatePropertyForm
from flask_login import login_user, current_user, logout_user, login_required, AnonymousUserMixin

# Declare the blueprints
proprety = Blueprint('proprety', __name__)


# Write the endpoints for properties
@proprety.route('/property/add', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def create_property():
    """ Allows the owner to add a property """
    # Checking if the current user is authenticated
    if not current_user.is_authenticated or isinstance(current_user, AnonymousUserMixin):
        flash('You have to be logged in before you can post a property!', 'warning')
        return redirect(url_for("#"))
    
    # We check if the current_user is a Tenant
    if isinstance(current_user, Tenant):
        flash('You can not post a Job!', 'danger')
        return redirect(url_for("#"))
    
    # if the current_user is an Owner
    form = PropertyForm()
    if form.validate_on_submit():
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        location = request.form.get('location')
        property_type = request.form.get('property_type')
        bedrooms = request.form.get('bedrooms')
        bathrooms = request.form.get('bathrooms')
        size = request.form.get('size')
        amenities = request.form.get('amenities')
        available_from = request.form.get('available_from')

        new_property = Property(
            title=title,
            description=description,
            price=price,
            location=location,
            property_type=property_type,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            size=size,
            amenities=amenities,
            available_from=available_from,
            owner_id=current_user.id
        )

        db.session.add(new_property)
        db.session.commit()

        # return jsonify({'message': 'Property posted successfully', 'property': new_property.id}), 201
        flash('Property posted successfully', 'success')
        return redirect(url_for('#dasboard'))
    render_template('#create_property.html', form=form)
    


@proprety.route('/property/<int:property_id>/update', methods=['GET', 'POST'], strict_slashes=False)
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

@proprety.route('/property/<int:property_id>/delete', methods=['GET', 'POST'])
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


@proprety.route('/property/<int:property_id>/view', methods=['GET', 'POST'], strict_slashes=False)
def view_property(property_id):
    """ Allows the tenant to view a property """
    prop = Property.query.get_or_404(property_id)
    render_template('#view_property.html', title=prop.title, property=prop)
    # return jsonify({'property': property}), 200
    

@proprety.route('/property/search', methods=['GET', 'POST'], strict_slashes=False)
# @login_required
def search_properties():
    # Search for properties
    # Seems we will allow any user to search for properties but hold them when they want to appy for the property
    location = request.args.get('location')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    property_type = request.args.get('property_type')
    property_status = request.args.get('property_status')  # sale or rent
    min_bedrooms = request.args.get('min_bedrooms')
    min_bathrooms = request.args.get('min_bathrooms')
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))

    query = Property.query

    if location:
        query = query.filter(Property.location == location)
    if min_price:
        query = query.filter(Property.price >= min_price)
    if max_price:
        query = query.filter(Property.price <= max_price)
    if property_type:
        query = query.filter(Property.property_type == property_type)
    if property_status:
        query = query.filter(Property.property_status == property_status)
    if min_bedrooms:
        query = query.filter(Property.bedrooms >= min_bedrooms)
    if min_bathrooms:
        query = query.filter(Property.bathrooms >= min_bathrooms)

    properties = query.limit(limit).offset(offset).all()
    properties_list = [
        {
            'id': property.id,
            'title': property.title,
            'description': property.description,
            'price': property.price,
            'location': property.location,
            'property_type': property.property_type,
            'property_status': property.property_status,
            'bedrooms': property.bedrooms,
            'bathrooms': property.bathrooms,
            'size': property.size,
            'amenities': property.amenities,
            'available_from': property.available_from,
            'owner_id': property.owner_id,
            'created_at': property.created_at,
            'updated_at': property.updated_at
        }
        for property in properties
    ]
    # return jsonify(properties_list), 200
    render_template('#search_properties.html', properties=properties_list, limit=limit, offset=offset)


@app.route('/properties', methods=['GET'], strict_slashes=False)
@login_required
def get_properties():
    """ Get all properties """
    # Shows peoperty in batches on page
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)

    properties = Property.query.offset(offset).limit(limit).all()
    total_properties = Property.query.count()

    return render_template('properties.html', properties=properties, total=total_properties, limit=limit, offset=offset)

@app.route('/dashboard', methods=['GET'], strict_slashes=False)
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

@app.route('/property/<int:property_id>/apply', methods=['GET', 'POST'], strict_slashes=False)
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