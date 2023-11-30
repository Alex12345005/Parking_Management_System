from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from .. import crud, schemas, models
from ..database import get_db

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

@router.get("/get_user/{email}", response_model=schemas.Users)
def get_user(email: str, db: Session = Depends(get_db)):
    """
    Get user details by email.

    Args:
        email (str): Email of the user.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.Users: The user details.
    """
    user = crud.get_user_by_email(db, email)
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

@router.options("/post_user/", response_model=None)
def options_post_user():
    return {}