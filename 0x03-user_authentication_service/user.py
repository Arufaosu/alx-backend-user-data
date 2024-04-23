#!/usr/bin/env python3
"""User.py"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """The User model mapped to the `users` table"""

    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))

    def __repr__(self):
        """Representation of the user instance"""
        return f'User ({self.id}): {self.email} - {self.hashed_password}'
