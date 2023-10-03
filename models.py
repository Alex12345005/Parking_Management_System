from peewee import *
from database import conn

import datetime

class BaseModel(Model):
    class Meta:
        database = conn

class login_credentials(BaseModel):
    id = CharField(unique=True, max_length=100, primary_key=True)
    username = TextField(unique=True, max_length=30)
    password = TextField(max_length=40)

    class Meta:
        db_table = 'login_credentials'

class vehicle_info(BaseModel):
    id = CharField(max_length=100, primary_key=True)
    license_plate = TextField(max_length=10)
    name = TextField(max_length=30)
    parking_time = CharField(max_length=40)

    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = 'vehicle_info'