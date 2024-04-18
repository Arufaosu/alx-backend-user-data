#!/usr/bin/env python3
"""The Auth class"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Class to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Return True `path` is not in `excluded_paths`"""

        if not path or not excluded_paths:
            return True

        if not path.endswith('/'):
            path += '/'

        for ex_path in excluded_paths:

            if ex_path.endswith('/'):
                if path == ex_path:
                    return False

            elif ex_path.endswith('*'):
                if path[:len(ex_path) - 1] == ex_path[:-1]:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """Return the value of the header request"""
        if request:
            return request.headers.get('Authorization', None)
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """To be implemented by BasicAuth or SessionAuth subclasses"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value (session ID) from a request"""

        if not request:
            return None

        cookie_name = os.getenv('SESSION_NAME')

        return request.cookies.get(cookie_name)
