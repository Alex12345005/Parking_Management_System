from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.post("/create_parking_permission/", response_model=schemas.ParkingPermission)
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

@router.get("/get_parking_permissions/", response_model=list[schemas.ParkingPermission])
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
