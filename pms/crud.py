"""Module defining CRUD (Create, Read, Update, Delete) operations for the parking management system."""

import bcrypt
from sqlalchemy.orm import Session
from .models import Vehicle, Tag, ParkingPermission, LoginCredentials
from .schemas import (
    LoginCredentialsCreate, TagCreate, ParkingPermissionCreate, VehicleCreate
)

# 1. get_vehicle_by_id
def get_vehicle_by_id(db: Session, vehicle_id: int):
    """
    Retrieve a vehicle by its ID.

    Args:
        db (Session): SQLAlchemy database session.
        vehicle_id (int): The ID of the vehicle.

    Returns:
        Vehicle: The retrieved vehicle.
    """
    return db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()


# 2. get_vehicle_by_name
def get_vehicle_by_name(db: Session, owner_name: str):
    """
    Retrieve a vehicle by its owner's name.

    Args:
        db (Session): SQLAlchemy database session.
        owner_name (str): The owner's name.

    Returns:
        Vehicle: The retrieved vehicle.
    """
    return db.query(Vehicle).filter(Vehicle.owner_name == owner_name).first()


# 3. get_vehicle_by_plate
def get_vehicle_by_plate(db: Session, license_plate: str):
    """
    Retrieve a vehicle by its license plate.

    Args:
        db (Session): SQLAlchemy database session.
        license_plate (str): The license plate of the vehicle.

    Returns:
        Vehicle: The retrieved vehicle.
    """
    return db.query(Vehicle).filter(Vehicle.license_plate == license_plate).first()


# 4. get_vehicle
def get_vehicle(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of vehicles with optional pagination.

    Args:
        db (Session): SQLAlchemy database session.
        skip (int): Number of items to skip.
        limit (int): Number of items to retrieve.

    Returns:
        List[Vehicle]: List of retrieved vehicles.
    """
    return db.query(Vehicle).offset(skip).limit(limit).all()


# 5. create_vehicle
def create_vehicle(db: Session, vehicle: VehicleCreate):
    """
    Create a new vehicle entry.

    Args:
        db (Session): SQLAlchemy database session.
        vehicle (VehicleCreate): Pydantic schema representing the vehicle data.

    Returns:
        Vehicle: The created vehicle.
    """
    db_vehicle = Vehicle(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


# 6. create_user
def create_user(db: Session, user: LoginCredentialsCreate):
    """
    Create a new user entry with a hashed password.

    Args:
        db (Session): SQLAlchemy database session.
        user (LoginCredentialsCreate): Pydantic schema representing the user data.

    Returns:
        LoginCredentials: The created user.
    """
    hashed_password = hash_password(user.password)
    db_user = LoginCredentials(username=user.username, password=hashed_password, is_active=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_login_credentials(db: Session, skip: int = 0, limit: int = 100) -> list[LoginCredentials]:
    """
    Retrieve a list of login credentials with optional pagination.

    Args:
        db (Session): SQLAlchemy database session.
        skip (int): Number of items to skip.
        limit (int): Number of items to retrieve.

    Returns:
        List[LoginCredentials]: List of retrieved login credentials.
    """
    return db.query(LoginCredentials).offset(skip).limit(limit).all()


# 7. create_tag
def create_tag(db: Session, tag: TagCreate):
    """
    Create a new tag entry.

    Args:
        db (Session): SQLAlchemy database session.
        tag (TagCreate): Pydantic schema representing the tag data.

    Returns:
        Tag: The created tag.
    """
    db_tag = Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


# 8. create_parking_permission
def create_parking_permission(db: Session, permission: ParkingPermissionCreate):
    """
    Create a new parking permission entry.

    Args:
        db (Session): SQLAlchemy database session.
        permission (ParkingPermissionCreate): Pydantic schema representing the parking permission data.

    Returns:
        ParkingPermission: The created parking permission.
    """
    db_permission = ParkingPermission(**permission.dict())
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def get_parking_permission(db: Session, permission_id: int):
    """
    Retrieve a parking permission by its ID.

    Args:
        db (Session): SQLAlchemy database session.
        permission_id (int): The ID of the parking permission.

    Returns:
        ParkingPermission: The retrieved parking permission.
    """
    return db.query(ParkingPermission).filter(ParkingPermission.parking_permission_id == permission_id).first()

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with a generated salt.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    # Generate a secure salt and use it to hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')