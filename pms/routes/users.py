from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from .. import crud, schemas, models
from ..database import get_db
from typing import List


router = APIRouter()
    
@router.post("/post_user/", response_model=schemas.Users)
def create_user(user_info: schemas.UsersCreate, db: Session = Depends(get_db)):
    """
    Create a new vehicle entry.

    Args:
        vehicle_info (schemas.VehicleCreate): Pydantic schema representing the vehicle data.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.Vehicle: The created vehicle.
    """
    created_user_info = crud.create_user(db, user_info)
    return created_user_info

@router.get("/get_user/{username}", response_model=schemas.Users)
def get_user(username: str, db: Session = Depends(get_db)):
    """
    Get user details by username.

    Args:
        email (str): username of the user.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.Users: The user details.
    """
    user = crud.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/get_salt/{username}", response_model=str)
def get_salt(username: str, db: Session = Depends(get_db)):
    """
    Get the salt for a user by username.

    Args:
        username (str): Username of the user.
        db (Session): SQLAlchemy database session.

    Returns:
        str: The salt for the user.
    """
    salt = crud.get_salt_by_username(db, username)
    if salt is None:
        raise HTTPException(status_code=404, detail="Salt not found for the user")
    return salt

@router.get("/get_users/", response_model=List[schemas.Users])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of vehicles with optional pagination.

    Args:
        skip (int): Number of items to skip.
        limit (int): Number of items to retrieve.
        db (Session): SQLAlchemy database session.

    Returns:
        List[schemas.Vehicle]: List of retrieved vehicles.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.options("/post_user/", response_model=None)
def options_post_user():
    return {}

@router.options("/get_users/", response_model=None)
def options_get_user():
    return {}