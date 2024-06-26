#!/usr/bin/env python3
"""Module of Session Authentication views
"""
from api.v1.views import app_views
from flask import jsonify, make_response, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Return the JSON representation of the logged user
    """

    email = request.form.get('email')
    if not email:
        return jsonify({'error': 'email missing'}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({'error': 'password missing'}), 400

    try:
        user = User.search({'email': email})[0]
    except BaseException:
        return jsonify({'error': 'no user found for this email'}), 404

    if not user.is_valid_password(password):
        return jsonify({'error': 'wrong password'}), 401

    else:
        from api.v1.app import auth

        session_id = auth.create_session(user.id)

        response = make_response(user.to_json())
        response.set_cookie(getenv('SESSION_NAME'), session_id)

        return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """Return an empty JSON dict if the session has been deleted successfully
    """
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        abort(404)
