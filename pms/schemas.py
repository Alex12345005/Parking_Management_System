import datetime
from pydantic import BaseModel
from typing import List
from .models import *
from datetime import datetime as dt



# Define schema for Vehicle
class VehicleBase(BaseModel):
    owner_name: str
    license_plate: str
    tag_id: int
    parking_permission_id: int

class VehicleCreate(BaseModel):
    owner_name: str
    license_plate: str

class Vehicle(BaseModel):
    vehicle_id: int
    owner_name: str
    license_plate: str
    tag_id: int
    parking_permission_id: int
    created_at: dt
    updated_at: dt

    class Config:
        """Configuration for Vehicle schema."""
        from_attributes = True
        arbitrary_types_allowed = True

# Define schema for Login Credentials
class LoginCredentialsBase(BaseModel):
    """Base schema for creating login credentials."""
    username: str
    password: str

class LoginCredentialsCreate(LoginCredentialsBase):
    """Schema for creating login credentials."""
    username: str
    password: str

class LoginCredentials(LoginCredentialsBase):
    """Schema for reading login credentials."""
    id: int
    is_active: bool

    class Config:
        """Configuration for LoginCredentials schema."""
        from_attributes = True
        arbitrary_types_allowed = True

# Define schema for Tag
class TagBase(BaseModel):
    """Base schema for creating a Tag."""
    tag_name: str

class TagCreate(TagBase):
    """Schema for creating a Tag."""
    tag_name: str

class Tag(TagBase):
    """Schema for reading a Tag."""
    tag_id: int
    vehicle: Vehicle  # Adjusted to represent one-to-one relationship

    class Config:
        """Configuration for Tag schema."""
        from_attributes = True
        arbitrary_types_allowed = True

# Define schema for ParkingPermission
class ParkingPermissionBase(BaseModel):
    """Base schema for creating a ParkingPermission."""
    start_time: dt
    end_time: dt

class ParkingPermissionCreate(ParkingPermissionBase):
    """Schema for creating a ParkingPermission."""
    start_time: dt
    end_time: dt

class ParkingPermission(ParkingPermissionBase):
    """Schema for reading a ParkingPermission."""
    parking_permission_id: int

    class Config:
        """Configuration for ParkingPermission schema."""
        from_attributes = True
        arbitrary_types_allowed = True