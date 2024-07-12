#!/usr/bin/python3
""" The base class for all models in the application """
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String,Text, Date, func, Boolean
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship, Mapped
from app import Base
from enum import Enum
from flask_login import UserMixin


class Owner(Base, UserMixin):
    """ The user model

    Args:
        Base (_type_): Onwers models
    """
    __tablename__ = 'owners'
    id = Column(Integer, primary_key=True)
    username = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    phone = Column(String(128), nullable=False)
    image_file = Column(String(128), nullable=False, default='default.jpg')
    location = Column(String(128), nullable=False)
    property_id = relationship('Property', backref='owners', lazy=True)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.location}', '{self.phone}')"


    def get_id(self):
        """ Get the user id"""
        return self.id

    
class Tenant(Base, UserMixin):
    """ The tenant model

    Args:
        Base (_type_): Having a separate table so we can allow tenants to have their own account
    """
    __tablename__ = 'tenants'
    id = Column(Integer, primary_key=True)
    username = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    phone = Column(String(128), nullable=False)
    image_file = Column(String(128), nullable=False, default='default.jpg')
    location = Column(String(128), nullable=False)
    
    def __repr__(self):
        return f"Tenant('{self.username}', '{self.email}', '{self.image_file}', '{self.location}', '{self.phone}')"
    
    def get_id(self):
        """ Get the tenant id"""
        return self.id


class TenantProperty(Base):
    """ The tenant property model

    Args:
        Base (_type_): We we connect the property to the tenant
        using many to many relationship
        A tenant can rent many properties and a property can be rented by many tenants

    Returns:
        _type_: A relationship between the tenant and the property
    """
    __tablename__ = 'tenant_properties'
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    property_id = Column(Integer, ForeignKey('properties.id'))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_assigned = Column(Boolean, default=False)
    
    tenants = relationship('Tenant', backref='tenant_properties')
    propertys = relationship('Property', backref='tenant_properties')


class PropertyStatus(Enum):
    """ The property status model

    Args:
        Enum (_type_): _description_
        UserMixin (_type_): session management
    """
    SALE = "sale"
    RENT = "rent"
    SOLD = "sold"
    RENTED = "rented"

class Property(Base):
    """ The property model

    Args:
        Base (_type_): _description_
        UserMixin (_type_): _description_

    Returns:
        _type_: _description_
    """
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(200), nullable=False)
    price = Column(Integer, nullable=False)
    property_type = Column(String(200), nullable=False)
    property_status = Mapped[PropertyStatus]
    bathrooms = Column(Integer, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    available_from = Column(DateTime, nullable=False, default=func.current_timestamp())
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('owners.id'))
    
    def __repr__(self):
        return f"Property('{self.title}', '{self.description}', '{self.location}', '{self.price}', '{self.property_type}', '{self.property_status}', '{self.bathrooms}', '{self.bedrooms}', '{self.size}')"    
    
    
   
class Messages(Base, UserMixin):
    """Message model

    Args:
            Base (_type_): _description_
    """
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    # sender_id = Column(Integer, ForeignKey('users.id'))
    # receiver_id = Column(Integer, ForeignKey('users.id'))
    property_id = Column(Integer, ForeignKey('properties.id'))
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Messages('{self.sender_id}', '{self.receiver_id}', '{self.property_id}', '{self.message}')"
