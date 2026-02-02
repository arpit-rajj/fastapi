from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models
from app.main import app
from app.databases import get_db
import pytest

SQLALCHEMY_TEST_DATABASE_URL = "postgresql://postgres:arpitraj%40020415@localhost:5432/test_db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
Test_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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


@pytest.fixture # make a global test user available to all tests
def test_user(client):
    response = client.post("/users/", json={"email": "test@example.com",
                                            "password": "password123"})
    assert response.status_code == 201
    data = response.json()
    data["password"] = "password123"
    return data

@pytest.fixture
def token(test_user):
    from app.oauth2 import create_access_token
    return create_access_token(data={"user_id": test_user['id']})
@pytest.fixture
def authorized_client(client, token):
    # return a client instance that includes the Authorization header
    authed = client
    authed.headers = {**authed.headers, "Authorization": f"Bearer {token}"}
    return authed


@pytest.fixture
def unauthorized_client(client):
    """Explicit fixture for an unauthenticated client (useful for posts/all tests)."""
    return client

@pytest.fixture
def test_posts(test_user, session):
    posts_data = [{
        "title": "Test Post",
        "content": "This is a test post",
        "owner_id": test_user['id']
    },
    {
        "title": "Test Post 2",
        "content": "This is another test post",
        "owner_id": test_user['id']
    },
    {
        "title": "Test Post 3",
        "content": "This is yet another test post",
        "owner_id": test_user['id']
    }]
    def create_post_model(post):
        return models.Post(**post)
    post_map=map(create_post_model, posts_data)
    posts=list(post_map)
    session.add_all(posts)  
    session.commit()
    posts = session.query(models.Post).all()
    return posts