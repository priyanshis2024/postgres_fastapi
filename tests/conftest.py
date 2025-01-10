from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app import schemas
from app.configure import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db,Base
from app.oauth2 import create_access_token
# SQLALCHEMY_DATABASE_URL = "postgresql://<user_name>:<password>@<ip-address/hostname>/<database_name>"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


# Dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# @pytest.fixture
# def session():
    # Base.metadata.drop_all(bind=engine) # drop the table and then run test and code
    # Base.metadata.create_all(bind=engine) # create the table and then run the test
    # db = TestingSessionLocal()
    # try:
        # yield db
    # finally:
        # db.close()

# @pytest.fixture
# def client(session):
#     def override_get_db():
#         try:
#             yield session
#         finally:
#             session.close()
#     app.dependency_overrides[get_db] = override_get_db
#     yield TestClient(app)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"Email": "callmephone@gmail.com",
                 "Password": "password123"}
    res = client.post("/users/",json=user_data)
    assert res.status_code == 201
    return res.json()

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client,token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client