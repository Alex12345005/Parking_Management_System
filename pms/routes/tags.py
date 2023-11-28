from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.post("/create_tag/", response_model=schemas.Tag)
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