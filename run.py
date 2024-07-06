#!/usr/bin/python3
""" The flask application entry point """
from app import app

if __name__ == '__main__':
    app.run(debug=True)
