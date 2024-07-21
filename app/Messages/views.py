from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import db, socketio
from app.models import Messages, Users, Property
from .forms import ReplyForm
from flask_login import current_user, login_required, AnonymousUserMixin
from flask_socketio import emit

# Declare the blueprints
messages = Blueprint('messages', __name__, url_prefix="/messages", template_folder='templates', static_folder='static')


@messages.route('/', methods=['GET', 'POST'], strict_slashes=False)
def allmessages():
    """ The messages page """
    if not current_user.is_authenticated:
        flash('You have to be logged in before you can send a message!', 'warning')
        return redirect(url_for("main.home"))
    
    users = Users.query.filter(Users.id != current_user.id).all()
    received_messages = Messages.query.filter_by(receiver_id=current_user.id).all()
    unread_count = Messages.query.filter_by(receiver_id=current_user.id, read=False).count()

    return render_template('message.html', users=users, received_messages=received_messages, unread_count=unread_count)


@messages.route('/<int:message_id>', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def view_message(message_id):
    message = Messages.query.get_or_404(message_id)
    sender = Users.query.get_or_404(message.sender_id)
    property_details = Property.query.get_or_404(message.property_id)
    reply_form = ReplyForm()

    # Get the full conversation
    conversation = Messages.query.filter(
        (Messages.sender_id == current_user.id) | (Messages.receiver_id == current_user.id),
        (Messages.sender_id == sender.id) | (Messages.receiver_id == sender.id),
        Messages.property_id == message.property_id
    ).order_by(Messages.timestamp).all()

    if reply_form.validate_on_submit():
        new_message = Messages(
            sender_id=current_user.id,
            receiver_id=message.sender_id,
            message=reply_form.message.data,
            property_id=message.property_id
        )
        db.session.add(new_message)
        db.session.commit()
        # flash('Reply sent!', 'success')
        return redirect(url_for('messages.view_message', message_id=message.id))

    message.read = True  # Mark the message as read when it is viewed
    db.session.commit()

    return render_template('view_messages.html', message=message, sender=sender, property_details=property_details, reply_form=reply_form, conversation=conversation)




@socketio.on('send_message')
def handle_send_message(data):
    if not current_user.is_authenticated or isinstance(current_user, AnonymousUserMixin):
        # Notify client to redirect to login page
        emit('authentication_error', {
            'message': 'You need to be logged in to send a message.'
        })
        return

    sender_id = current_user.id
    property_id = data.get('property_id')

    # Query the Property model to get the property object
    prop = Property.query.get(property_id)

    if sender_id == prop.owner_id:
        # If the sender is the owner of the property, do nothing
        emit('authentication_error', {'message': 'You cannot send a message to yourself.'})
        return

    receiver_id = data['receiver_id']

    new_message = Messages(
        sender_id=sender_id,
        receiver_id=receiver_id,
        message=data['content'],
        property_id=property_id
    )
    db.session.add(new_message)
    db.session.commit()

    emit('receive_message', {
        'sender': new_message.sender.username,
        'content': new_message.message,
        'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'message_id': new_message.id
    }, room=str(receiver_id))
    flash('Message sent!', 'success')





@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        emit('join', {'user_id': current_user.id})
