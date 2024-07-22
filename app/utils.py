<<<<<<< HEAD
=======
#!/usr/bin/python3
""" we will use here for urls for the homepage"""
from flask import render_template, url_for, flash, redirect, request, Blueprint
from app.models import Tenant, Property, Owner, Messages
from flask_login import current_user, logout_user, login_required

# Declare the blueprints
main = Blueprint('main', __name__, url_prefix="/home", template_folder='templates', static_folder='static')


@main.route('/', methods=['GET', 'POST'], strict_slashes=False)
def home():
    """Homepage"""
    unread_count = 0
    if current_user.is_authenticated:
        unread_count = Messages.query.filter_by(receiver_id=current_user.id, read=False).count()
    
    recent_properties = Property.query.order_by(Property.created_at.desc()).limit(6).all()
    
    return render_template('home.html', unread_count=unread_count, recent_properties=recent_properties)


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
        flash('No Signed in Account! Pls sign in first', 'warning')
        return redirect(url_for('main.home'))
<<<<<<< HEAD
>>>>>>> 8ed179db4ccce604927cf581f887b2c4630d868a
=======
>>>>>>> origin/main
>>>>>>> 147b6bacaaf3b300b443e7ec10095c592b97d748
