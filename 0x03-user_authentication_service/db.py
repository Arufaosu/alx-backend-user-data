#!/usr/bin/env python3
"""DB.py"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Dict
from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database"""

        user = User()

        user.email = email
        user.hashed_password = hashed_password

        self._session.add(user)
        self._session.commit()

        return user

    @staticmethod
    def check_keys(kwargs: Dict) -> None:
        """Check kwargs keys are valid User attributes"""

        valid_keys = ['id', 'email', 'hashed_password',
                      'session_id', 'reset_token']

        for key in kwargs.keys():

            if key not in valid_keys:
                raise InvalidRequestError

    def find_user_by(self, **kwargs) -> User:
        """Find and return the first user"""

        user = self._session.query(User).filter_by(**kwargs).first()

        self.check_keys(kwargs)

        if not user:
            raise NoResultFound

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update the user’s attributes"""

        user = self.find_user_by(id=user_id)

        try:
            self.check_keys(kwargs)
        except InvalidRequestError:
            raise ValueError

        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()

