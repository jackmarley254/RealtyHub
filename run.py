#!/usr/bin/python3
""" The flask application entry point """
from app import app, socketio

if __name__ == '__main__':
    socketio.run(app, debug=True)
