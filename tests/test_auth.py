import json
import pytest

from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine, StaticPool

from db import get_session
from main import app

client = TestClient(app=app)

user_1 = {"username": "mani", "password": "pass"}
user_2 = {"username": "reza", "password": "1234"}


def test_signup(client: TestClient):
    # Test user signup
    response = client.post("/auth/signup", json=user_1)
    assert response.status_code == 200


def test_signup_duplicate(client: TestClient):
    # Test duplicate signup
    client.post("/auth/signup", json=user_2)
    response = client.post("/auth/signup", json=user_2)
    assert response.status_code == 400 or response.status_code == 409


def test_login_success(client: TestClient):
    # Ensure user exists
    client.post("/auth/signup", json=user_1)
    # Test login
    response = client.post("/auth/login", json=user_1)
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_failure(client: TestClient):
    # Test login with wrong password
    client.post("/auth/signup", json=user_2)
    wrong_password = {"username": user_2["username"], "password": "wrongpass"}
    response = client.post("/auth/login", json=wrong_password)
    assert response.status_code == 401


def test_me_route(client: TestClient):
    # Signup and login to get token
    client.post("/auth/signup", json=user_1)
    login_resp = client.post("/auth/login", json=user_1)
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/user/profile", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user_1["username"]
