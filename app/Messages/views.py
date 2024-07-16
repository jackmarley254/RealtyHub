#!/usr/bin/python3
""" The views for the application """
from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import db, socketio
from app.models import Messages, Messages, Users
from .forms import MessageForm
from flask_login import current_user, login_required, AnonymousUserMixin
from flask_socketio import emit

# Declare the blueprints
messages = Blueprint('messages', __name__, url_prefix="/messages", template_folder='templates', static_folder='static')


# Write the endpoints for messages

@messages.route("/messages", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def allmessages():
    if not current_user.is_authenticated or isinstance(current_user, AnonymousUserMixin):
        flash('You have to be logged in before you can send a message!', 'warning')
        return redirect(url_for("main.home"))
    
    form = MessageForm()
    form.recipient.choices = [(user.id, user.username) for user in Users.query.filter(Users.id != current_user.id).all()]

    if form.validate_on_submit():
        recipient_id = form.recipient.data
        content = form.content.data
        message = Messages(sender_id=current_user.id, receiver_id=recipient_id, content=content)
        db.session.add(message)
        db.session.commit()
        
        # Emit the message using SocketIO
        socketio.emit('receive_message', {
            'sender': current_user.username,
            'content': content
        }, room=recipient_id)
        
        flash('Message sent successfully!', 'success')
        return redirect(url_for('messages.allmessages'))

    users = Users.query.filter(Users.id != current_user.id).all()
    received_messages = Messages.query.filter_by(receiver_id=current_user.id).all()
    sent_messages = Messages.query.filter_by(sender_id=current_user.id).all()
    return render_template('message.html', users=users, received_messages=received_messages, sent_messages=sent_messages, form=form)

@messages.route("/send_message/<int:receiver_id>", methods=['GET', 'POST'])
@login_required
def send_message(receiver_id):
    form = MessageForm()
    receiver = Users.query.get_or_404(receiver_id)
    if form.validate_on_submit():
        message = Messages(sender_id=current_user.id, receiver_id=receiver.id, content=form.content.data)
        db.session.add(message)
        db.session.commit()
        flash('Your message has been sent!', 'success')
        return redirect(url_for('owner.messages'))
    return render_template('send_messages.html', form=form, receiver=receiver)

@socketio.on('send_message')
def handle_send_message(json):
    message = Messages(sender_id=json['sender_id'], receiver_id=json['receiver_id'], content=json['content'])
    db.session.add(message)
    db.session.commit()
    emit('receive_message', {'sender': message.sender.username, 'content': message.content}, broadcast=True)