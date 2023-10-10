from sqlalchemy.orm import Session

from . import models, schemas


def get_vehicle_by_id(db: Session, id: int):
    return db.query(models.VehicleInfo).filter(models.VehicleInfo.id == id).first()


def get_vehicle_by_name(db: Session, name: str):
    return db.query(models.VehicleInfo).filter(models.VehicleInfo.name == name).first()


def get_vehicle_by_plate(db: Session, license_plate: str):
    return db.query(models.VehicleInfo).filter(models.VehicleInfo.license_plate == license_plate).first()

def get_vehicle(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.VehicleInfo).offset(skip).limit(limit).all()

def create_vehicle(db: Session, vehicle_info: schemas.VehicleInfoCreate):
    db_vehicle_info = models.VehicleInfo(name=vehicle_info.name, license_plate = vehicle_info.license_plate, parking_time = vehicle_info.parking_time)
    db.add(db_vehicle_info)
    db.commit()
    db.refresh(db_vehicle_info)
    return db_vehicle_info

