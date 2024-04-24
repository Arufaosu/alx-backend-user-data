#!/usr/bin/env python3
"""app.py"""
from auth import Auth
from flask import (abort, Flask, jsonify, make_response,
                   redirect, request, url_for)


app = Flask(__name__)

app.url_map.strict_slashes = False

AUTH = Auth()


@app.route('/')
def index():
    """root"""
    return make_response(jsonify({'message': 'Bienvenue'}))

@app.route('/users/', methods=['POST'])
def users():
    """End-point to register a user"""

    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400

    return make_response(jsonify({'email': email, 'message': 'user created'}))


@app.route('/sessions/', methods=['POST'])
def login():
    """Create a new login session for the user"""

    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)

    response = make_response(jsonify({'email': email, 'message': 'logged in'}))
    response.set_cookie('session_id', session_id)

    return response


@app.route('/sessions/', methods=['DELETE'])
def logout() -> str:
    """Destroy the session for the user"""

    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect(url_for('index'))


@app.route('/profile/')
def profile():
    """Return the user's email"""

    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    return make_response(jsonify({'email': user.email}))


@app.route('/reset_password/', methods=['POST'])
def get_reset_password_token():
    """Generate reset password token for a user"""

    email = request.form.get('email')

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return make_response(jsonify({'email': email,
                                  'reset_token': reset_token}))


@app.route('/reset_password/', methods=['PUT'])
def update_password():
    """Update the user's password"""

    email = request.form.get('email')
    password = request.form.get('password')
    reset_token = request.form.get('reset_token')

    if not email or not reset_token or not password:
        abort(403)

    try:
        AUTH.valid_reset_token(email, reset_token)

        AUTH.update_password(reset_token, password)
    except ValueError:
        abort(403)

    return make_response(jsonify({'email': email,
                                  'message': 'Password updated'}))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
