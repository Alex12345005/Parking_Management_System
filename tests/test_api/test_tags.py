import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pms.database import Base, get_db
from pms.main import app
from pms.models import Tag
from pms import schemas

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

@pytest.fixture(scope="function")
def test_db_session(client):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

def test_create_tag(client, test_db_session):
    tag_data = {"TagName": "TestTag"}
    response = client.post("/tags/create_tag/", json=tag_data)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["TagName"] == tag_data["TagName"]
    assert "TagID" in data

def test_get_tags(client, test_db_session):
    response = client.get("/tags/get_tags/")
    assert response.status_code == 200
    tags = response.json()
    assert len(tags) > 0
