from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db
from .. import database

router = APIRouter()

@router.post("/create_tag/", response_model=schemas.Tag)
def create_tag(tag_create: schemas.TagCreate, db: Session = Depends(get_db)):
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

@router.get("/get_tags/", response_model=list[schemas.Tag])
def get_tags_route(db: Session = Depends(get_db)):
    """
    Get all tags.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        List of tags.
    """
    tags = crud.get_tags(db)
    return tags

@router.get("/get_tags_name/", response_model=list[str])
def get_tags_by_name(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """
    Get tags by name with optional pagination.

    Args:
        skip (int): Number of items to skip.
        limit (int): Number of items to retrieve.
        db (Session): SQLAlchemy database session.

    Returns:
        List of tag names.
    """
    tags = crud.get_tags_by_name(db, skip=skip, limit=limit)
    return tags

@router.options("/get_tags_name/", response_model=None)
def options_get_tags_name():
    """
    Provides options for the endpoint to retrieve tags by name.
    """
    return {}

@router.options("/get_tags/", response_model=None)
def options_get_tags():
    """
    Provides options for the endpoint to retrieve all tags.
    """
    return {}
