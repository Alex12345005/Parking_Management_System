from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from .models import *
from datetime import datetime as dt



# Define schema for Vehicle
class Vehicle(BaseModel):
    VehicleID: int
    LicensePlate: str
    UsersID: int
    TagID: int
    PermissionID: List[int]
    StartTime: datetime
    EndTime: datetime

class VehicleCreate(BaseModel):
    LicensePlate: str
    UsersID: int
    TagID: int
    PermissionID: List[int]
    StartTime: datetime
    EndTime: datetime

class VehicleUpdate(BaseModel):
    LicensePlate: Optional[str] = None
    UsersID: Optional[int] = None
    TagID: Optional[int] = None
    PermissionID: Optional[List[int]] = None
    StartTime: Optional[datetime] = None
    EndTime: Optional[datetime] = None

class Vehicle(BaseModel):
    VehicleID: int
    LicensePlate: str
    UsersID: int
    TagID: int
    PermissionID: List[int]
    StartTime: datetime
    EndTime: datetime

    class Config:
        """Configuration for Vehicle schema."""
        arbitrary_types_allowed = True
        from_attributes = True

# Define schema for Login Credentials
class UsersBase(BaseModel):
    """Base schema for creating login credentials."""
    Username: str
    Password: str
    Salt: str
    Email: str
    PhoneNumber: str

class UsersCreate(UsersBase):
    """Schema for creating login credentials."""
    Username: str
    Password: str
    Salt: str
    Email: str
    PhoneNumber: str

class Users(UsersBase):
    """Schema for reading login credentials."""
    UserID: int
    Username: str
    Password: str
    Salt: str
    Email: str
    PhoneNumber: str

    class Config:
        """Configuration for LoginCredentials schema."""
        from_attributes = True
        arbitrary_types_allowed = True

# Define schema for Tag
class TagBase(BaseModel):
    """Base schema for creating a Tag."""
    TagID: int
    TagName: str

class TagCreate(TagBase):
    """Schema for creating a Tag."""
    TagName: str

class Tag(TagBase):
    """Schema for reading a Tag."""
    TagID: int
    TagName: str

    class Config:
        """Configuration for Tag schema."""
        from_attributes = True
        arbitrary_types_allowed = True

# Define schema for ParkingPermission
class ParkingPermissionBase(BaseModel):
    """Base schema for creating a ParkingPermission."""
    PermissionType: str

class ParkingPermissionCreate(ParkingPermissionBase):
    """Schema for creating a ParkingPermission."""
    PermissionType: str


class ParkingPermission(ParkingPermissionBase):
    """Schema for reading a ParkingPermission."""
    PermissionID: int
    PermissionType: str

    class Config:
        """Configuration for ParkingPermission schema."""
        from_attributes = True
        arbitrary_types_allowed = True



class VehicleParkingPermissionBase(BaseModel):
    """Base schema for creating a VehicleParkingPermission."""
    VehicleParkingPermissionID: int
    PermissionID: int
    VehicleID: int


class VehicleParkingPermissionCreate(VehicleParkingPermissionBase):
    """Schema for creating a VehicleParkingPermission."""
    PermissionID: int
    VehicleID: int


class VehicleParkingPermission(VehicleParkingPermissionBase):
    """Schema for reading a VehicleParkingPermission."""
    VehicleParkingPermissionID: int
    PermissionID: int
    VehicleID: int

    class Config:
        """Configuration for VehicleParkingPermission schema."""
        from_attributes = True
        arbitrary_types_allowed = True

# Define schema for Log
class LogBase(BaseModel):
    """Base schema for creating a Log."""
    EntryTime: datetime
    ExitTime: datetime

class LogCreate(LogBase):
    """Schema for creating a Log."""
    EntryTime: datetime
    ExitTime: datetime


class Log(LogBase):
    """Schema for reading a Log."""
    PermissionID: int
    EntryTime: datetime
    ExitTime: datetime

    class Config:
        """Configuration for Log schema."""
        from_attributes = True
        arbitrary_types_allowed = True