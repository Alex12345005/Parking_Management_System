"""
Module defining CRUD (Create, Read, Update, Delete) operations for the parking management system.
"""

import bcrypt
import json
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .models import Vehicle, Tag, ParkingPermission, Users, VehicleParkingPermission
from .schemas import (
    UsersCreate, TagCreate, ParkingPermissionCreate, VehicleCreate, VehicleParkingPermissionCreate
)
from . import schemas
from . import models

def hash_password(Password: str) -> str:
    """
    Hash a password using bcrypt with a generated salt.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(Password.encode('utf-8'), salt)
    return (hashed_password.decode('utf-8'), salt)

def create_user(db: Session, user: UsersCreate):
    """
    Create a new user entry in the database.

    Args:
        db (Session): SQLAlchemy database session.
        user (UsersCreate): Pydantic schema representing the user data.

    Returns:
        Users: The created user.
    """
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
    Get a user by username.

    Args:
        db_session: The currently active connection to the database.
        username (str): Username of the user.

    Returns:
        Users: The user details or None if not found.
    """
    return db_session.query(models.Users).filter(models.Users.Username == username).first()

def get_user_by_id(db_session, user_id: int):
    """
    Get a user by ID.

    Args:
        db_session: The currently active connection to the database.
        user_id (int): ID of the user.

    Returns:
        Users: The user details or None if not found.
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
    """
    Create a new tag entry in the database.

    Args:
        db (Session): SQLAlchemy database session.
        tag (TagCreate): Pydantic schema representing the tag data.

    Returns:
        Tag: The created tag.
    """
    db_tag = Tag(
        TagName=tag.TagName,
    )
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def create_parking_permission(db: Session, permission: ParkingPermissionCreate):
    """
    Create a new parking permission entry in the database.

    Args:
        db (Session): SQLAlchemy database session.
        permission (ParkingPermissionCreate): Pydantic schema representing the parking permission data.

    Returns:
        ParkingPermission: The created parking permission.
    """
    db_permission = ParkingPermission(
        PermissionType=permission.PermissionType,
    )
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def get_tags(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of tags from the database with optional pagination.

    Args:
        db (Session): SQLAlchemy database session.
        skip (int): Number of items to skip.
        limit (int): Number of items to retrieve.

    Returns:
        List[Tag]: List of retrieved tags.
    """
    return db.query(models.Tag).offset(skip).limit(limit).all()

def get_tags_by_name(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of tag names from the database with optional pagination.

    Args:
        db (Session): SQLAlchemy database session.
        skip (int): Number of items to skip.
        limit (int): Number of items to retrieve.

    Returns:
        List[str]: List of retrieved tag names.
    """
    tags = db.query(models.Tag.TagName).offset(skip).limit(limit).all()
    tag_names = [tag[0] for tag in tags]
    return tag_names

def create_vehicle(db: Session, vehicle: VehicleCreate):
    """
    Create a new vehicle entry in the database.

    Args:
        db (Session): SQLAlchemy database session.
        vehicle (VehicleCreate): Pydantic schema representing the vehicle data.

    Returns:
        Vehicle: The created vehicle.
    """
    db_vehicle = Vehicle(
        LicensePlate=vehicle.LicensePlate,
        UsersID=vehicle.UsersID,
        TagID=vehicle.TagID,
        StartTime=vehicle.StartTime,
        EndTime=vehicle.EndTime
    )
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)

    for perm_id in vehicle.PermissionID:
        stored_perm: ParkingPermission | None = db.query(ParkingPermission).filter(
            ParkingPermission.PermissionID == perm_id
        ).first()

        if stored_perm is None:
            raise ValueError("One or more permissions do not exist.")

        db_vehicle_perm = VehicleParkingPermission(
            PermissionID=stored_perm.PermissionID,
            VehicleID=db_vehicle.VehicleID,
        )
        db.add(db_vehicle_perm)

    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def create_vehicle_parking_permission(db: Session, vehicle_parking_permission: VehicleParkingPermissionCreate):
    """
    Create a new vehicle parking permission entry in the database.

    Args:
        db (Session): SQLAlchemy database session.
        vehicle_parking_permission (VehicleParkingPermissionCreate): Pydantic schema representing the vehicle parking permission data.

    Returns:
        VehicleParkingPermission: The created vehicle parking permission.
    """
    db_vehicle_parking_permission = VehicleParkingPermission(
        PermissionID=vehicle_parking_permission.PermissionID,
        VehicleID=vehicle_parking_permission.VehicleID,
    )
    db.add(db_vehicle_parking_permission)
    db.commit()
    db.refresh(db_vehicle_parking_permission)
    return db_vehicle_parking_permission

def get_vehicles(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of vehicles from the database with optional pagination.

    Args:
        db (Session): SQLAlchemy database session.
        skip (int): Number of items to skip.
        limit (int): Number of items to retrieve.

    Returns:
        List[Vehicle]: List of retrieved vehicles.
    """
    db_vehicles_to_return = []
    all_db_vehicles:list[models.Vehicle] = db.query(models.Vehicle).offset(skip).limit(limit).all()
    for db_vehicle in all_db_vehicles:
        perm_id = []
        vehicle_id = db_vehicle.VehicleID
        db_vehicle_perms:list[models.VehicleParkingPermission] = db.query(models.VehicleParkingPermission).filter(models.VehicleParkingPermission.VehicleID == vehicle_id).all()
        for db_perm in db_vehicle_perms:
            perm_id.append(db_perm.PermissionID)
        new_vehicle = schemas.Vehicle(VehicleID=vehicle_id, LicensePlate=db_vehicle.LicensePlate, UsersID=db_vehicle.UsersID, TagID=db_vehicle.TagID, StartTime=db_vehicle.StartTime, EndTime=db_vehicle.EndTime, PermissionID=perm_id.copy())
        db_vehicles_to_return.append(new_vehicle)
    return db_vehicles_to_return

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of users from the database with optional pagination.

    Args:
        db (Session): SQLAlchemy database session.
        skip (int): Number of items to skip.
        limit (int): Number of items to retrieve.

    Returns:
        List[Users]: List of retrieved users.
    """
    return db.query(models.Users).offset(skip).limit(limit).all()

def get_parking_permissions(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of parking permissions from the database with optional pagination.

    Args:
        db (Session): SQLAlchemy database session.
        skip (int): Number of items to skip.
        limit (int): Number of items to retrieve.

    Returns:
        List[ParkingPermission]: List of retrieved parking permissions.
    """
    return db.query(models.ParkingPermission).offset(skip).limit(limit).all()

def update_vehicle(db: Session, vehicle_id: int, vehicle_update: schemas.VehicleUpdate):
    """
    Update a vehicle in the database.

    Args:
        db (Session): SQLAlchemy database session.
        vehicle_id (int): ID of the vehicle to update.
        vehicle_update (VehicleUpdate): Pydantic schema representing the vehicle update data.

    Returns:
        Vehicle: The updated vehicle or None if not found.
    """
    db_vehicle = db.query(models.Vehicle).filter(models.Vehicle.VehicleID == vehicle_id).first()
    if db_vehicle is None:
        return None

    for var, value in vars(vehicle_update).items():
        if value is not None and var != "PermissionID":
            setattr(db_vehicle, var, value)

    db.query(models.VehicleParkingPermission).filter(models.VehicleParkingPermission.VehicleID == vehicle_id).delete()

    if vehicle_update.PermissionID is not None:
        for perm_id in vehicle_update.PermissionID:
            new_vehicle_perm = models.VehicleParkingPermission(
                VehicleID=vehicle_id,
                PermissionID=perm_id
            )
            db.add(new_vehicle_perm)

    db.commit()
    
    perm_id = []
    vehicle_id = db_vehicle.VehicleID
    db_vehicle_perms = db.query(models.VehicleParkingPermission).filter(models.VehicleParkingPermission.VehicleID == vehicle_id).all()
    for db_perm in db_vehicle_perms:
        perm_id.append(db_perm.PermissionID)
    api_vehicle = schemas.Vehicle(
        VehicleID=vehicle_id, 
        LicensePlate=db_vehicle.LicensePlate, 
        UsersID=db_vehicle.UsersID, 
        TagID=db_vehicle.TagID, 
        StartTime=db_vehicle.StartTime, 
        EndTime=db_vehicle.EndTime, 
        PermissionID=perm_id.copy()
    )

    return api_vehicle

def get_vehicle_by_id(db: Session, vehicle_id: int):
    """
    Retrieve a vehicle by ID.

    Args:
        db (Session): SQLAlchemy database session.
        vehicle_id (int): ID of the vehicle to retrieve.

    Returns:
        Vehicle: The retrieved vehicle or None if not found.
    """
    return db.query(models.Vehicle).filter(models.Vehicle.VehicleID == vehicle_id).first()

def delete_vehicle_by_id(db: Session, vehicle_id: int):
    """
    Delete a vehicle by ID.

    Args:
        db (Session): SQLAlchemy database session.
        vehicle_id (int): ID of the vehicle to delete.
    """
    db.query(models.VehicleParkingPermission).filter(models.VehicleParkingPermission.VehicleID == vehicle_id).delete()

    db.query(models.Vehicle).filter(models.Vehicle.VehicleID == vehicle_id).delete()
    db.commit()
