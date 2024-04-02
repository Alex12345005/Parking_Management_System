import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, orm
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from pms.database import Base, get_db
from pms.main import app

# Ihre Datenbank und FastAPI-App-Konfiguration
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    Base.metadata.drop_all(bind=engine)

def create_user(client):
    user_data = {
        "Username": "TestUser",
        "Password": "testpass",
        "Salt": "some_salt_value",
        "Email": "test@example.com",
        "PhoneNumber": "1234567890"
    }
    response = client.post("/users/post_user/", json=user_data)
    assert response.status_code == 200
    return response.json()["UserID"]

def create_tag(client):
    tag_data = {"TagName": "TestTag"}
    response = client.post("/tags/create_tag/", json=tag_data)  # Pfad entsprechend anpassen
    assert response.status_code == 200
    return response.json()["TagID"]

def create_permission(client):
    permission_data = {"PermissionType": "TestPermission"}
    response = client.post("/parking_permissions/create_parking_permission/", json=permission_data)  # Pfad entsprechend anpassen
    assert response.status_code == 200
    return response.json()["PermissionID"]

def test_create_vehicle(client):
    users_id = create_user(client)
    tag_id = create_tag(client)
    permission_id = create_permission(client)

    start_time = datetime.now().isoformat()  # Convert to ISO format string
    end_time = (datetime.now() + timedelta(days=1)).isoformat()  # Convert to ISO format string

    vehicle_data = {
        "LicensePlate": "ABC123",
        "UsersID": users_id,
        "TagID": tag_id,
        "PermissionID": [permission_id],
        "StartTime": start_time,
        "EndTime": end_time,
    }

    response = client.post("/vehicles/post_vehicle/", json=vehicle_data)
    assert response.status_code == 200
    data = response.json()
    assert data["LicensePlate"] == vehicle_data["LicensePlate"]

def test_get_vehicles(client):
    response = client.get("/vehicles/get_vehicles/")
    assert response.status_code == 200
    vehicles = response.json()
    assert isinstance(vehicles, list)
