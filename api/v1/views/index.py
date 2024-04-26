#!/usr/bin/python3
"""API index views module"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """ function for status route that returning status """
    status = {
        "status": "OK"
    }
    return jsonify(status)
