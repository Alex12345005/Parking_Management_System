"""Module defining CRUD (Create, Read, Update, Delete) operations for the parking management system."""

import bcrypt
from typing import Optional
from pydantic import BaseModel
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

def create_tag(db: Session, tag: TagCreate):
    db_tag = Tag(
        TagName=tag.TagName,
    )
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def create_parking_permission(db: Session, permission: ParkingPermissionCreate):
    db_permission = ParkingPermission(
        PermissionType=permission.PermissionType,
    )
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def get_tags(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tag).offset(skip).limit(limit).all()

def get_tags_by_name(db: Session, skip: int = 0, limit: int = 100):
    tags = db.query(models.Tag.TagName).offset(skip).limit(limit).all()
    tag_names = [tag[0] for tag in tags]
    return tag_names

def create_vehicle(db: Session, vehicle: VehicleCreate):
    db_vehicle = Vehicle(
        LicensePlate=vehicle.LicensePlate,
        UsersID=vehicle.UsersID,  
        TagID=vehicle.TagID,
        PermissionID=vehicle.PermissionID,
        StartTime=vehicle.StartTime,
        EndTime=vehicle.EndTime
    )
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def get_vehicles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vehicle).offset(skip).limit(limit).all()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Users).offset(skip).limit(limit).all()

def get_parking_permissions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ParkingPermission).offset(skip).limit(limit).all()