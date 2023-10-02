from peewee import *

user = 'root'
password = 'root'
db_name = 'pms_db'

conn = MySQLDatabase(
    db_name, user=user,
    password=password,
    host='localhost'
)

class BaseModel(Model):
    class Meta:
        Database = conn