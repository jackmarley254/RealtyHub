<<<<<<< HEAD
=======
#!/usr/bin/python3
""" we will use here for urls for the homepage"""
from flask import render_template, url_for, flash, redirect, request, Blueprint
from app.models import Tenant, Property, Owner
from flask_login import current_user, logout_user, login_required

# Declare the blueprints
main = Blueprint('main', __name__, url_prefix="/home", template_folder='templates', static_folder='static')


@main.route('/', methods=['GET', 'POST'], strict_slashes=False)
def home():
    """ homepage """
    return render_template('home.html')

@main.route('/logout')
@login_required
def logout():
    """remove the username from the session if it's there"""
    logout_user()
    flash(f'You have been logged out!', 'warning')
    return redirect(url_for('main.home'))

@main.route('/accounts')
def accounts():
    """Checks the instance and routes the user to the account"""
    
    # Log the type of current_user
    print(f"current_user type: {current_user}")
    
    if isinstance(current_user, Owner):
        return redirect(url_for('owner.account'))
    elif isinstance(current_user, Tenant):
        return redirect(url_for('tenant.accounts'))
    # Handle unexpected user types
    else:
        flash('Unexpected user type!', 'warning')
        return redirect(url_for('main.home'))
>>>>>>> origin/main
