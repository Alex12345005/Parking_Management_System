"""
Main module for the parking management system using FastAPI.

This module initializes the FastAPI application and sets up the database. It defines API endpoints for creating and retrieving vehicles, login credentials, tags, and parking permissions.

Dependencies:
    - FastAPI
    - SQLAlchemy

Modules:
    - crud: Defines CRUD operations for interacting with the database.
    - models: Defines SQLAlchemy models for the parking management system.
    - schemas: Defines Pydantic schemas for data validation and serialization.
    - database: Configures the database connection.

Endpoints:
    - POST /post_vehicle/: Create a new vehicle entry.
    - GET /get_vehicle/: Retrieve a list of vehicles with optional pagination.
    - GET /get_vehicle_by_id/{id}: Retrieve a vehicle by its ID.
    - POST /login_credentials/: Create a new user entry with a hashed password.
    - GET /get_login_credentials/: Retrieve a list of login credentials with optional pagination.
    - POST /create_tag/: Create a new tag entry.
    - POST /create_parking_permission/: Create a new parking permission entry.
    - GET /get_parking_permissions/: Retrieve a list of parking permissions with optional pagination.

"""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    """
    Get a database session.

    Yields:
        Session: SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/post_vehicle/", response_model=schemas.Vehicle)
def create_vehicle_info(vehicle_info: schemas.VehicleCreate, db: Session = Depends(get_db)):
    """
    Create a new vehicle entry.

    Args:
        vehicle_info (schemas.VehicleCreate): Pydantic schema representing the vehicle data.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.Vehicle: The created vehicle.
    """
    created_vehicle_info = crud.create_vehicle(db, vehicle_info)
    return created_vehicle_info

@app.get("/get_vehicle/", response_model=list[schemas.Vehicle])
def read_vehicle(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of vehicles with optional pagination.

    Args:
        skip (int): Number of items to skip.
        limit (int): Number of items to retrieve.
        db (Session): SQLAlchemy database session.

    Returns:
        List[schemas.Vehicle]: List of retrieved vehicles.
    """
    vehicle_info = crud.get_vehicle(db, skip=skip, limit=limit)
    return vehicle_info


@app.get("/get_vehicle_by_id/{id}", response_model=schemas.Vehicle)
def read_vehicle_by_id(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a vehicle by its ID.

    Args:
        id (int): The ID of the vehicle.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.Vehicle: The retrieved vehicle.
    """
    vehicle_info = crud.get_vehicle_by_id(db, id=id)
    if vehicle_info is None:
        raise HTTPException(status_code=404, detail="User not found")
    return vehicle_info


@app.post("/login_credentials/", response_model=schemas.LoginCredentials)
def create_user(user_create: schemas.LoginCredentialsCreate, db: Session = Depends(get_db)):
    """
    Create a new user entry with a hashed password.

    Args:
        user_create (schemas.LoginCredentialsCreate): Pydantic schema representing the user data.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.LoginCredentials: The created user.
    """
    user = crud.create_user(db, user_create)
    return user

@app.get("/get_login_credentials/", response_model=list[schemas.LoginCredentials])
def read_login_credentials(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of login credentials with optional pagination.

    Args:
        skip (int): Number of items to skip.
        limit (int): Number of items to retrieve.
        db (Session): SQLAlchemy database session.

    Returns:
        List[schemas.LoginCredentials]: List of retrieved login credentials.
    """
    login_credentials = crud.get_login_credentials(db, skip=skip, limit=limit)
    return login_credentials

@app.post("/create_tag/", response_model=schemas.Tag)
def create_tag_endpoint(tag_create: schemas.TagCreate, db: Session = Depends(get_db)):
    """
    Create a new tag entry.

    Args:
        tag_create (schemas.TagCreate): Pydantic schema representing the tag data.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.Tag: The created tag.
    """
    tag = crud.create_tag(db, tag_create)
    return tag

@app.post("/create_parking_permission/", response_model=schemas.ParkingPermission)
def create_parking_permission_endpoint(permission_create: schemas.ParkingPermissionCreate, db: Session = Depends(get_db)):
    """
    Create a new parking permission entry.

    Args:
        permission_create (schemas.ParkingPermissionCreate): Pydantic schema representing the parking permission data.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.ParkingPermission: The created parking permission.
    """
    permission = crud.create_parking_permission(db, permission_create)
    return permission

@app.get("/get_parking_permissions/", response_model=list[schemas.ParkingPermission])
def get_parking_permissions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of parking permissions with optional pagination.

    Args:
        skip (int): Number of items to skip.
        limit (int): Number of items to retrieve.
        db (Session): SQLAlchemy database session.

    Returns:
        List[schemas.ParkingPermission]: List of retrieved parking permissions.
    """
    permissions = crud.get_parking_permission(db, skip=skip, limit=limit)
    return permissions
