#!/usr/bin/env python3
"""auth.py"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
import uuid
from user import User


class Auth:
    """Auth class"""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user in the database"""

        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            pass

        user = self._db.add_user(email, _hash_password(password))

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Check the credentials"""

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            return True
        else:
            return False

    def create_session(self, email: str) -> str:
        """Create a session ID"""

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Takes a single `session_id` string argument
        and returns the corresponding User or None"""

        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy the user's session"""

        try:

            self._db.update_user(user_id, session_id=None)

        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate reset password token"""

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()

        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update the user's password"""

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_password = _hash_password(password)
        self._db.update_user(user.id,
                             hashed_password=hashed_password,
                             reset_token=None)


def _hash_password(password: str) -> bytes:
    """Hash `password` and returns a hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    return str(uuid.uuid4())
