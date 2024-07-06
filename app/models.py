#!/usr/bin/python3
""" The base class for all models in the application """
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String,Text, Date, func
from sqlalchemy.types import JSON
from app import Base
from enum import Enum


class User(Base):
    """ The user model

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    phone = Column(String(128), nullable=False)
    image_file = Column(String(128), nullable=False, default='default.jpg')
    location = Column(String(128), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.location}', '{self.phone}')"

class Property(Base):
    """ The property model

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(200), nullable=False)
    price = Column(Integer, nullable=False)
    property_type = Column(String(200), nullable=False)
    property_status = Column(String(200), nullable=False)
    bathrooms = Column(Integer, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    # amenties = Column(JSON, nullable=False)
    available_from = Column(DateTime, nullable=False, default=func.current_timestamp())
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # We create a one to many relationship between the user and the property
    # A user can own many properties and a property can be owned by one user
    owner_id = Column(Integer, ForeignKey('users.id'))
    
    def __repr__(self):
        return f"Property('{self.title}', '{self.description}', '{self.location}', '{self.price}', '{self.property_type}', '{self.property_status}', '{self.bathrooms}', '{self.bedrooms}', '{self.size}')"    
    
    
   
class Messages(Base):
    """Message model

    Args:
            Base (_type_): _description_
    """
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))
    property_id = Column(Integer, ForeignKey('properties.id'))
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Messages('{self.sender_id}', '{self.receiver_id}', '{self.property_id}', '{self.message}')"
        
class PropertyStatus(Enum):
    """Property status enum

    Args:
        Enum (_type_): _description_
    """
    SALE = "sale"
    RENT = "rent"
    SOLD = "sold"
    RENTED = "rented"
