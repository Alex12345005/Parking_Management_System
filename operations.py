import peewee
from models import *

if __name__ == '__main__':
    try:
        conn.connect()
        vehicle_info.create_table()
        login_credentials.create_table()
    except peewee.InternalError as px:
        print(str(px))