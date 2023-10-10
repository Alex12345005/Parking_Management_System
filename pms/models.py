import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base

class LoginCredentials(Base):
    __tablename__ = 'login_credentials'

    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String(30), unique=True)
    password = Column(String(40))

class VehicleInfo(Base):
    __tablename__ = 'vehicle_info'

    id = Column(Integer, primary_key=True)
    license_plate = Column(String(10))
    name = Column(String(30))
    parking_time = Column(String(40))
    created_at = Column(DateTime, default=datetime.datetime.now)