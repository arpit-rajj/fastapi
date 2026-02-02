from app.oauth2 import SECRET_KEY,ALGORITHM 
import jwt
import pytest
from app import schema, models

@pytest.fixture # Create a test user and return its data to test next functions
def test_user(client):
    response = client.post("/users/", json={"email": "test@example.com",
                                            "password": "password123"})
    assert response.status_code == 201
    data = response.json()
    data["password"] = "password123"
    return data

def test_create_user(client):
    response = client.post("/users/", json={"email": "test2@example.com",
                                            "password": "password123"})
    assert response.status_code == 201    
    data = schema.Userresponse(**response.json())
    assert data.email == "test2@example.com"

def test_user_login(client, test_user):
    response = client.post("/login/",data={"username": test_user['email'],
                                           "password": test_user['password']})
    assert response.status_code == 200
    login_data = schema.Token(**response.json())
    payload = jwt.decode(login_data.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    id= payload.get("user_id")
    assert id == test_user['id']
    assert login_data.token_type == "bearer"
@pytest.mark.parametrize("email,password,status_code", [
    ("wrongemail@example.com","password123",403),
    ("test@example.com","wrongpassword",403),
    ("wrongemail@example.com","wrongpassword",403),
    ("","",422),
    ("test@example.com","",422),
    ("","password123",422)
])
def test_incorrect_login(client, email, password, status_code):
    response = client.post("/login/",data={"username": email,
                                           "password": password})
    assert response.status_code == status_code
    # assert response.json().get("detail") == "Invalid Credentials"