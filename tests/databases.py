from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models
from app.main import app
from app.databases import get_db
import pytest

SQLALCHEMY_TEST_DATABASE_URL = "postgresql://postgres:arpitraj%40020415@localhost:5432/test_db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
Test_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine,expire_on_commit=False)

# @pytest.fixture(scope="module") scope to define how many times the fixture is invoked
@pytest.fixture()
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = Test_SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@pytest.fixture()
def client(session):
    def override_get_db():
        db = Test_SessionLocal()
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)