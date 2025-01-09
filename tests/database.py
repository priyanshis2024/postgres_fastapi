from fastapi.testclient import TestClient
import pytest
from app.main import app
from app import schemas
from app.configure import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db,Base

# SQLALCHEMY_DATABASE_URL = "postgresql://<user_name>:<password>@<ip-address/hostname>/<database_name>"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

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