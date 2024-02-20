from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..database import get_db
from typing import List


router = APIRouter()

@router.post("/post_vehicle/", response_model=schemas.Vehicle)
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

@router.get("/get_vehicles/", response_model=List[schemas.Vehicle])
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
    vehicles = crud.get_vehicles(db, skip=skip, limit=limit)
    return vehicles

@router.delete("/delete_vehicle/{id}")
def delete_vehicle_endpoint(id: int, db: Session = Depends(get_db)):
    vehicle = crud.get_vehicle_by_id(db, id)
    if vehicle:
        crud.delete_vehicle_by_id(db, id)
        return {"message": f"Vehicle with ID {id} has been deleted."}
    else:
        raise HTTPException(status_code=404, detail=f"Vehicle with ID {id} not found.")

@router.put("/update_vehicles/{vehicle_id}", response_model=schemas.Vehicle)
async def update_vehicle(vehicle_id: int, vehicle_update: schemas.VehicleUpdate, db: Session = Depends(get_db)):
    updated_vehicle = crud.update_vehicle(db, vehicle_id, vehicle_update)
    print("API2 %s" % update_vehicle)
    if updated_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return updated_vehicle

@router.options("/post_vehicle/", response_model=None)
def options_post_vehicle():
    return {}

@router.options("/delete_vehicle/{id}", response_model=None)
def options_delete_vehicle():
    return {}