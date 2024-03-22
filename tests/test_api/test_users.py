from fastapi.testclient import TestClient
from sqlalchemy import create_engine, orm
from sqlalchemy.orm import sessionmaker
from pms.database import Base, get_db
from pms.main import app
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db_session():
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    def _get_test_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client

def test_create_user(client, test_db_session):
    response = client.post("/users/post_user/", json={
        "Username": "testuser",
        "Password": "testpassword",
        "Salt": "somesalt",
        "Email": "test@example.com",
        "PhoneNumber": "1234567890"
    })
    assert response.status_code == 200

def test_read_users(client, test_db_session):
    client.post("/users/post_user/", json={
        "Username": "anotheruser",
        "Password": "testpassword",
        "Salt": "somesalt",
        "Email": "another@example.com",
        "PhoneNumber": "1234567891"
    })

    response = client.get("/users/get_users/?skip=0&limit=1")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) >= 1
