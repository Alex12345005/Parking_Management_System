import json
import os
import shutil
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from pms import models
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.get("/backup-database")
async def export_database_json(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    vehicles = db.query(models.Vehicle).all()
    
    vehicles_data = [vehicle.to_dict() for vehicle in vehicles]
    
    database_data = {
        "vehicles": vehicles_data
    }
    
    database_json = json.dumps(database_data, ensure_ascii=False, indent=4)
    
    temp_file_name = "./temp_database_export.json"
    with open(temp_file_name, "w", encoding="utf-8") as temp_file:
        temp_file.write(database_json)
    
    return FileResponse(path=temp_file_name, filename="database_export.json", media_type='application/json')

@router.post("/check-license")
async def check_license(LicensePlate: str, db: Session = Depends(get_db)):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.LicensePlate == LicensePlate).first()
    if vehicle:
        return {"exists": True}
    else:
        return {"exists": False}