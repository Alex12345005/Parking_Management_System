import datetime
from pydantic import BaseModel
from typing import List

#Define schema for Login Credentials
class LoginCredentialsBase(BaseModel):
    username: str
    password: str

class LoginCredentialsCreate(LoginCredentialsBase):
    username: str
    password: str

class LoginCredentials(LoginCredentialsBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

#Define schema for Vehicle Info
class VehicleInfoBase(BaseModel):
    license_plate: str
    name: str
    parking_time: str

class VehicleInfoCreate(VehicleInfoBase):
    license_plate: str
    name: str
    parking_time: str

class VehicleInfo(VehicleInfoBase):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True
