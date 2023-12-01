"""Module defining CRUD (Create, Read, Update, Delete) operations for the parking management system."""

import bcrypt
from typing import Optional
from sqlalchemy.orm import Session
from .models import Vehicle, Tag, ParkingPermission, Users
from .schemas import (
    UsersCreate, TagCreate, ParkingPermissionCreate, VehicleCreate
)
from . import models

def hash_password(Password: str) -> str:
    """
    Hash a password using bcrypt with a generated salt.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    # Generate a secure salt and use it to hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(Password.encode('utf-8'), salt)
    return (hashed_password.decode('utf-8'), salt)

def create_user(db: Session, user: UsersCreate):
#    hashed_password, salt = hash_password(user.Password)  # Assuming you have a hash_password function
    db_user = Users(
        Username=user.Username,
        Password=user.Password,
        Salt=user.Salt,
        Email=user.Email,
        PhoneNumber=user.PhoneNumber,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db_session, username: str):
    """
    Get a user by email
    :param db_session: The currently active connection to the database
    :param email: E-Mail of the user
    :return: User object or None
    """
    return db_session.query(models.Users).filter(models.Users.Username == username).first()

def get_user_by_id(db_session, user_id: int):
    """
    Get a user by ID
    :param db_session: The currently active connection to the database
    :param user_id: ID of the user
    :return: User object or None
    """
    return db_session.query(models.Users).filter(models.Users.UserID == user_id).first()

def get_salt_by_username(db: Session, username: str) -> Optional[str]:
    """
    Retrieve the salt for a user based on their username.

    Args:
        db (Session): SQLAlchemy database session.
        username (str): Username of the user.

    Returns:
        Optional[str]: The salt if the user is found, otherwise None.
    """
    user = db.query(Users).filter(Users.Username == username).first()
    if user:
        return user.Salt
    return None
