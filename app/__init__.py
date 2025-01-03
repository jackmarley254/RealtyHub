#!/usr/bin/python3
""" database init """
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO


app = Flask(__name__)

app.config['SECRET_KEY'] = 'RealtyHubapp'

# Configuration for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
Base = db.Model
bcrypt = Bcrypt(app)
socketio = SocketIO(app)

# Initialize the login manager
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.blueprint_login_views = {
    'tenant': 'tenant.login',
    'owner': 'owner.login'
}
login_manager.session_protection = "strong"


# Import the routes
from app.Property.views import proprety
from app.Tenant.views import tenant
from app.Owner.views import owner
from app.Messages.views import messages
from app.utils import main
from app.models import Tenant, Owner



@login_manager.user_loader
def load_user(user_id):
    """ Loads the user

    Args:
        user_id (_type_): The user id

    Returns:
        _type_: The user id
    """
    x = Owner.query.get(str(user_id))
    if x == None:
        x = Tenant.query.get(str(user_id))
        
    return x


# Register the blueprints
app.register_blueprint(proprety)
app.register_blueprint(tenant)
app.register_blueprint(owner)
app.register_blueprint(messages)
app.register_blueprint(main)
