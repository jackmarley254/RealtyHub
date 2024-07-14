# Real Estate Web Application 
--------

## This README file provides a comprehensive guide to your real estate web application, covering the introduction, project structure, features, database models, API endpoints, frontend implementation, authentication and authorization, and authors.
---------

## Table of Contents
- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Features](#features)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)
- [Frontend Implementation](#frontend-implementation)
- [Authentication and Authorization](#authentication-and-authorization)
- [Authors](#authors)

## Introduction
This real estate web application allows users to buy, sell, rent, and post properties. Built using React.js for the frontend, Flask for the backend, and MySQL for the database, it supports user registration, authentication, and features like property search, messaging, and property management.

## Features
- User Registration and Authentication
- Property Management (Post, Edit, Delete)
- Property Search with Filters
- Messaging System
- User Dashboard
- Email Notifications
- Mobile Responsiveness

## Database Models
### User Model
 ```python
from your_application import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    properties = db.relationship('Property', backref='owner', lazy=True)
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy=True)

----------------


### Property Model

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    property_type = db.Column(db.String(50), nullable=False)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    size = db.Column(db.Float)
    amenities = db.Column(db.String(200))
    available_from = db.Column(db.Date)
    status = db.Column(db.String(50), default='available')
    photos = db.relationship('Photo', backref='property', lazy=True)
    messages = db.relationship('Message', backref='property', lazy=True)


### Photo Model

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)

### Message Model
from datetime import datetime

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


## Authentication Endpoints

### Register
POST /api/register

Request:
{
    "username": "example",
    "email": "example@example.com",
    "password": "password123"
}

### Login
POST /api/login

Request:
{
    "email": "example@example.com",
    "password": "password123"
}


### Authors
- George
- Godswill
- [Jackson](jackndiritu97@gmail.com)
- Janefrancis
