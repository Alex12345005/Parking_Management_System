from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, TIMESTAMP, func
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base
from sqlalchemy.orm import Mapped

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

    Vehicle: Mapped["Vehicle"] = relationship('Vehicle', uselist=False, back_populates='Users')

class Tag(Base):
    """Model representing a tag for vehicle."""
    __tablename__ = 'tag'

    TagID: Mapped[int] = Column(Integer, primary_key=True)
    TagName: Mapped[str] = Column(String(30), unique=True)

    # Add a one-to-one relationship with Vehicle
    Vehicle: Mapped["Vehicle"] = relationship('Vehicle', uselist=False, back_populates='Tag')

class ParkingPermission(Base):
    """Model representing parking permissions for vehicle."""
    __tablename__ = 'parking_permission'

    PermissionID: Mapped[int] = Column(Integer, primary_key=True)
    PermissionType: Mapped[str] = Column(String(30), unique=True)

    Vehicle: Mapped["Vehicle"] = relationship('Vehicle', uselist=False, back_populates='ParkingPermission')

class Vehicle(Base):
    """Model representing a vehicle and its associated information."""
    __tablename__ = 'vehicle'

    VehicleID: Mapped[int] = Column(Integer, primary_key=True)
    LicensePlate: Mapped[str] = Column(String(10), unique=True)
    StartTime: Mapped[str] = Column(DateTime)
    EndTime: Mapped[str] = Column(DateTime)

    Log: Mapped["Log"] = relationship('Log', uselist=False, back_populates='Vehicle')
    
    #ForeignKeys
    TagID: Mapped[int] = Column(Integer, ForeignKey('tag.TagID'))
    Tag: Mapped["Tag"] = relationship('Tag', back_populates='Vehicle')

    UsersID: Mapped[int] = Column(Integer, ForeignKey('users.UserID'))
    Users: Mapped["Users"] = relationship('Users', back_populates='Vehicle')
    
    PermissionID: Mapped[int] = Column(Integer, ForeignKey('parking_permission.PermissionID'))
    ParkingPermission: Mapped["ParkingPermission"] = relationship('ParkingPermission', back_populates='Vehicle')


class Log(Base):
    """Model representing a tag for vehicle."""
    __tablename__ = 'log'

    LogID: Mapped[int] = Column(Integer, primary_key=True)
    EntryTime: Mapped[str] = Column(DateTime)
    ExitTime: Mapped[str] = Column(DateTime)

    # Add a one-to-one relationship with Vehicle
    VehicleID: Mapped[int] = Column(Integer, ForeignKey('vehicle.VehicleID'))
    Vehicle: Mapped["Vehicle"] = relationship('Vehicle', back_populates='Log')