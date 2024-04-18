#!/usr/bin/env python3
"""The SessionExpAuth class"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv
from models.user import User


class SessionExpAuth(SessionAuth):
    """Class to manage the Session Authentication"""

    user_id_by_session_id = {}

    def __init__(self):
        """Set the duration of Expiration time"""
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Create and return a Session ID for a `user_id`
        """

        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dict = {}
        session_dict['user_id'] = user_id
        session_dict['created_at'] = datetime.now()

        self.user_id_by_session_id[session_id] = session_dict

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID
        """

        if session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id[session_id]

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        if 'created_at' not in session_dict:
            return None

        exp_time = timedelta(seconds=self.session_duration)
        if datetime.now() > session_dict['created_at'] + exp_time:
            return None

        return session_dict.get('user_id')
