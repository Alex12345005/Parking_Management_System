from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.post("/login_credentials/", response_model=schemas.LoginCredentials)
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

@router.get("/get_login_credentials/", response_model=list[schemas.LoginCredentials])
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