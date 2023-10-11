from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/vehicle_info/", response_model=schemas.VehicleInfo)
def create_vehicle_info(vehicle_info: schemas.VehicleInfoCreate, db: Session = Depends(get_db)):
    created_vehicle_info = crud.create_vehicle(db, vehicle_info)
    return created_vehicle_info


@app.get("/vehicle_info/", response_model=list[schemas.VehicleInfo])
def read_vehicle(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vehicle_info = crud.get_vehicle(db, skip=skip, limit=limit)
    return vehicle_info


@app.get("/vehicle_info/{id}", response_model=schemas.VehicleInfo)
def read_vehicle_by_id(id: int, db: Session = Depends(get_db)):
    vehicle_info = crud.get_vehicle_by_id(db, id=id)
    if vehicle_info is None:
        raise HTTPException(status_code=404, detail="User not found")
    return vehicle_info


@app.post("/login_credentials/", response_model=schemas.LoginCredentials)
def create_user(user_create: schemas.LoginCredentialsCreate, db: Session = Depends(get_db)):
    user = crud.create_user(db, user_create)
    return user
