from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db
from .. import database

router = APIRouter()

@router.post("/post_vehicle_parking_permission/", response_model=schemas.VehicleParkingPermission)
def create_vehicle_parking_permission(vehicle_parking_permission_info: schemas.VehicleParkingPermissionCreate, db: Session = Depends(get_db)):

    created_vehicle_parking_permission_info = crud.create_vehicle_parking_permission(db, vehicle_parking_permission_info)
    return created_vehicle_parking_permission_info

@router.options("/post_vehicle_parking_permission/", response_model=None)
def options_post_vehicle_parking_permission():
    return {}