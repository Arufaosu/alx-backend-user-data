#!/usr/bin/env python3
"""The SessionAuth class"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import uuid


class SessionAuth(Auth):
    """Class to manage the Session Authentication for our API"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create and return a Session ID for a `user_id`
        """

        if not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID"""

        if not isinstance(session_id, str):
            return None

        user_id = self.user_id_by_session_id.get(session_id)

        return user_id

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve the User instance for a request"""

        if not request:
            return None

        session_id = self.session_cookie(request)

        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """Deletes the user session"""

        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        if not self.user_id_for_session_id(session_id):
            return False

        del self.user_id_by_session_id[session_id]
        return True
