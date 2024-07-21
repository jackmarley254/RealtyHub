#!/usr/bin/python3
""" The views for the application """
from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.models import User, Property
from app.routes.forms import RegisterForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
