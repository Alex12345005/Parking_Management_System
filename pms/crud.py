import bcrypt

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


def hash_password(password: str) -> str:
    # Generieren Sie ein sicheres Salz und verwenden Sie es zum Hashen des Passworts
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def create_user(db: Session, user_create: schemas.LoginCredentialsCreate):
    # Hashen Sie das Passwort, bevor Sie es in der Datenbank speichern
    hashed_password = hash_password(user_create.password)
    
    db_user = models.LoginCredentials(username=user_create.username, password=hashed_password, is_active=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user