from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, TIMESTAMP, func
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base
from sqlalchemy.orm import Mapped
from typing import Optional

class Users(Base):
    """Model representing the login credentials."""
    __tablename__ = 'users'

    UserID: Mapped[int] = Column(Integer, primary_key=True, unique=True)
    Username: Mapped[str] = Column(String(30), unique=True)
    Password: Mapped[str] = Column(String(40))
    Salt: Mapped[str] = Column(String(40))
    Email: Mapped[str] = Column(String(60), unique=True)
    PhoneNumber: Mapped[str] = Column(String(40))

    IsAdmin: Mapped[bool] = Column(Boolean, default=False)


class Tag(Base):
    """Model representing a tag for vehicle."""
    __tablename__ = 'tag'

    TagID: Mapped[int] = Column(Integer, primary_key=True)
    TagName: Mapped[str] = Column(String(30), unique=True)


class ParkingPermission(Base):
    """Model representing parking permissions for vehicle."""
    __tablename__ = 'parking_permission'

    PermissionID: Mapped[int] = Column(Integer, primary_key=True)
    PermissionType: Mapped[str] = Column(String(30), unique=True)


class VehicleParkingPermission(Base):
    """Model representing parking permissions for a vehicle."""
    __tablename__ = 'vehicle_parking_permission'

    VehicleParkingPermissionID = Column(Integer, primary_key=True)


    VehicleID = Column(Integer, ForeignKey('vehicle.VehicleID'))

    PermissionID = Column(Integer, ForeignKey('parking_permission.PermissionID')) 


class Vehicle(Base):
    """Model representing a vehicle and its associated information."""
    __tablename__ = 'vehicle'

    VehicleID: Mapped[int] = Column(Integer, primary_key=True)
    LicensePlate: Mapped[str] = Column(String(10), unique=True)
    StartTime: Mapped[str] = Column(DateTime)
    EndTime: Mapped[str] = Column(DateTime)
    
    TagID = Column(Integer, ForeignKey('tag.TagID')) 

    UsersID = Column(Integer, ForeignKey('users.UserID')) 

    Username = Column(Integer, ForeignKey('users.Username'))

    PermissionID = Column(Integer, ForeignKey('parking_permission.PermissionID'))

    def to_dict(self):
        return {
            "licenseplate": self.LicensePlate,
            "starttime": self.StartTime.isoformat() if self.StartTime else None,
            "endtime": self.EndTime.isoformat() if self.EndTime else None,
        }



class Log(Base):
    """Model representing a tag for vehicle."""
    __tablename__ = 'log'

    LogID: Mapped[int] = Column(Integer, primary_key=True)
    EntryTime: Mapped[str] = Column(DateTime)
    ExitTime: Mapped[str] = Column(DateTime)

    VehicleID = Column(Integer, ForeignKey('vehicle.VehicleID')) 
