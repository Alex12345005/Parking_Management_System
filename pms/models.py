from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, TIMESTAMP, func
from sqlalchemy.orm import relationship
from datetime import datetime as dt, timedelta

from .database import Base
from sqlalchemy.orm import Mapped

class LoginCredentials(Base):
    """Model representing the login credentials."""
    __tablename__ = 'login_credentials'

    id: Mapped[int] = Column(Integer, primary_key=True, unique=True)
    username: Mapped[str] = Column(String(30), unique=True)
    password: Mapped[str] = Column(String(40))
    is_active: Mapped[bool] = Column(Boolean, default=True)

class Tag(Base):
    """Model representing a tag for vehicles."""
    __tablename__ = 'tag'

    tag_id: Mapped[int] = Column(Integer, primary_key=True)
    tag_name: Mapped[str] = Column(String(30), unique=True)

    # Add a one-to-one relationship with Vehicle
    vehicle: Mapped["Vehicle"] = relationship('Vehicle', uselist=False, back_populates='tag')

class ParkingPermission(Base):
    """Model representing parking permissions for vehicles."""
    __tablename__ = 'parking_permission'

    parking_permission_id: Mapped[int] = Column(Integer, primary_key=True)
    start_time: Mapped[dt] = Column(TIMESTAMP, default=func.now())
    end_time: Mapped[dt] = Column(TIMESTAMP)

    vehicle: Mapped["Vehicle"] = relationship('Vehicle', uselist=False, back_populates='parking_permission')

class Vehicle(Base):
    """Model representing a vehicle and its associated information."""
    __tablename__ = 'vehicles'

    vehicle_id: Mapped[int] = Column(Integer, primary_key=True)
    owner_name: Mapped[str] = Column(String(30))
    license_plate: Mapped[str] = Column(String(10), unique=True)

    tag_id: Mapped[int] = Column(Integer, ForeignKey('tag.tag_id'))
    tag: Mapped["Tag"] = relationship('Tag', back_populates='vehicle')

    parking_permission_id: Mapped[int] = Column(Integer, ForeignKey('parking_permission.parking_permission_id'))
    parking_permission: Mapped["ParkingPermission"] = relationship('ParkingPermission', back_populates='vehicle')

    created_at: Mapped[dt] = Column(DateTime, default=dt.utcnow)
    updated_at: Mapped[dt] = Column(DateTime, default=dt.utcnow, onupdate=dt.utcnow)
