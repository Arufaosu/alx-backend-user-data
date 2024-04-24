#!/usr/bin/env python3
"""Testing the application routes
"""
import requests


def register_user(email: str, password: str) -> None:
    """Test registering a user
    """

    response = requests.post('http://localhost:5000/users',
                             data={'email': email, 'password': password})

    assert response.status_code == requests.codes.ok
    assert response.json() == {'email': email, 'message': 'user created'}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test logging in with wrong password
    """

    response = requests.post('http://localhost:5000/sessions',
                             data={'email': email, 'password': password})

    assert response.status_code == requests.codes.unauthorized


def log_in(email: str, password: str) -> str:
    """Test logging in correctly and return session ID
    """

    response = requests.post('http://localhost:5000/sessions',
                             data={'email': email, 'password': password})

    assert response.status_code == requests.codes.ok
    assert response.json() == {'email': email, 'message': 'logged in'}
    assert response.cookies.get('session_id') is not None

    return response.cookies['session_id']


def profile_unlogged() -> None:
    """Test 'GET /profile' with no session ID
    """

    response = requests.get('http://localhost:5000/profile')

    assert response.status_code == requests.codes.forbidden


def profile_logged(session_id: str) -> None:
    """Test 'GET /profile' with no session ID
    """

    jar = requests.cookies.RequestsCookieJar()
    jar.set('session_id', session_id)

    response = requests.get('http://localhost:5000/profile',
                            cookies=jar)

    assert response.status_code == requests.codes.ok
    assert response.json() == {'email': EMAIL}


def log_out(session_id: str) -> None:
    """Test logging out
    """

    jar = requests.cookies.RequestsCookieJar()
    jar.set('session_id', session_id)

    response = requests.delete('http://localhost:5000/sessions',
                               cookies=jar, allow_redirects=True)

    assert response.status_code == requests.codes.ok
    assert response.json() == {'message': 'Bienvenue'}


def reset_password_token(email: str) -> str:
    """Test 'POST /reset_password' route and return reset_token
    """

    response = requests.post('http://localhost:5000/reset_password',
                             data={'email': email})

    assert response.status_code == requests.codes.ok

    response_dict = response.json()
    assert response_dict['email'] == email

    reset_token = response_dict['reset_token']
    assert type(reset_token) is str

    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test 'PUT /reset_password' route
    """

    response = requests.put('http://localhost:5000/reset_password',
                            data={'email': email,
                                  'reset_token': reset_token,
                                  'password': new_password})

    assert response.status_code == requests.codes.ok
    assert response.json() == {'email': email, 'message': 'Password updated'}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
