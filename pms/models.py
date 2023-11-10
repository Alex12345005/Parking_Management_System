import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base

class LoginCredentials(Base):
    """Model representing the login credentials."""
    __tablename__ = 'login_credentials'

    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String(30), unique=True)
    password = Column(String(40))
    is_active = Column(Boolean, default=True)

    class Config:
        arbitrary_types_allowed = True

class Tag(Base):
    """Model representing a tag for vehicles."""
    __tablename__ = 'tags'

    tag_id = Column(Integer, primary_key=True)
    tag_name = Column(String(30), unique=True)

    # Add a one-to-one relationship with Vehicle
    vehicle = relationship('Vehicle', uselist=False, back_populates='tag')

class ParkingPermission(Base):
    """Model representing parking permissions for vehicles."""
    __tablename__ = 'parking_permission'

    parking_permission_id = Column(Integer, primary_key=True)
    start_time = Column(TIMESTAMP, default=datetime.datetime.now)
    end_time = Column(TIMESTAMP)

class Vehicle(Base):
    """Model representing a vehicle and its associated information."""
    __tablename__ = 'vehicles'

    vehicle_id = Column(Integer, primary_key=True)
    owner_name = Column(String(30))
    license_plate = Column(String(10), unique=True)

    tag_id = Column(Integer, ForeignKey('tags.tag_id'), unique=True)  # Make it a foreign key
    tag = relationship('Tag', back_populates='vehicle')

    parking_permission_id = Column(Integer, ForeignKey('parking_permission.parking_permission_id'))
    parking_permission = relationship('ParkingPermission', back_populates='vehicles')