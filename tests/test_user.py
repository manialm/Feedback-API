import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from db import get_session


def test_get_profile_success(client: TestClient, session: Session):
    """Test successful profile retrieval for authenticated user"""
    # First signup a user
    user_data = {"username": "testuser", "password": "testpass"}
    signup_response = client.post("/auth/signup", json=user_data)
    assert signup_response.status_code == 200
    
    # Login to get token
    login_response = client.post("/auth/login", json=user_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get profile
    response = client.get("/user/profile", headers=headers)
    assert response.status_code == 200
    profile_data = response.json()
    assert profile_data["username"] == "testuser"
    assert "id" in profile_data
    assert "password_hash" not in profile_data  # Should not expose password hash


def test_get_profile_unauthorized(client: TestClient, session: Session):
    """Test profile access without authentication"""
    response = client.get("/user/profile")
    assert response.status_code == 422  # FastAPI validation error for missing token


def test_get_profile_invalid_token(client: TestClient, session: Session):
    """Test profile access with invalid token"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/user/profile", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


def test_send_feedback_success(client: TestClient, session: Session):
    """Test successful feedback submission"""
    # First signup and login a user
    user_data = {"username": "testuser", "password": "testpass"}
    client.post("/auth/signup", json=user_data)
    login_response = client.post("/auth/login", json=user_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Submit feedback
    feedback_data = {
        "rating": 5,
        "comment": "Great service! Very helpful."
    }
    response = client.post("/user/feedback", json=feedback_data, headers=headers)
    assert response.status_code == 200
    
    feedback_response = response.json()
    assert feedback_response["rating"] == 5
    assert feedback_response["comment"] == "Great service! Very helpful."
    assert "id" in feedback_response
    assert "user_id" in feedback_response

@pytest.mark.skip()
def test_send_feedback_without_comment(client: TestClient, session: Session):
    """Test feedback submission with only rating"""
    # First signup and login a user
    user_data = {"username": "testuser", "password": "testpass"}
    client.post("/auth/signup", json=user_data)
    login_response = client.post("/auth/login", json=user_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Submit feedback with only rating
    feedback_data = {"rating": 8}
    response = client.post("/user/feedback", json=feedback_data, headers=headers)
    assert response.status_code == 200
    
    feedback_response = response.json()
    assert feedback_response["rating"] == 8
    assert feedback_response["comment"] is None


def test_send_feedback_without_rating(client: TestClient, session: Session):
    """Test feedback submission with only comment"""
    # First signup and login a user
    user_data = {"username": "testuser", "password": "testpass"}
    client.post("/auth/signup", json=user_data)
    login_response = client.post("/auth/login", json=user_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Submit feedback with only comment
    feedback_data = {"comment": "This is a test comment"}
    response = client.post("/user/feedback", json=feedback_data, headers=headers)
    assert response.status_code == 200
    
    feedback_response = response.json()
    assert feedback_response["rating"] == 1  # Default rating
    assert feedback_response["comment"] == "This is a test comment"



def test_send_feedback_unauthorized(client: TestClient, session: Session):
    """Test feedback submission without authentication"""
    feedback_data = {"rating": 5, "comment": "Test comment"}
    response = client.post("/user/feedback", json=feedback_data)
    assert response.status_code == 422  # FastAPI validation error for missing token


def test_send_feedback_invalid_token(client: TestClient, session: Session):
    """Test feedback submission with invalid token"""
    feedback_data = {"rating": 5, "comment": "Test comment"}
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.post("/user/feedback", json=feedback_data, headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"




@pytest.mark.skip()
def test_send_feedback_invalid_rating_too_low(client: TestClient, session: Session):
    """Test feedback submission with rating below minimum"""
    # First signup and login a user
    user_data = {"username": "testuser", "password": "testpass"}
    client.post("/auth/signup", json=user_data)
    login_response = client.post("/auth/login", json=user_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Submit feedback with invalid rating
    feedback_data = {"rating": 0, "comment": "Test comment"}
    response = client.post("/user/feedback", json=feedback_data, headers=headers)
    assert response.status_code == 422  # Validation error


@pytest.mark.skip()
def test_send_feedback_invalid_rating_too_high(client: TestClient, session: Session):
    """Test feedback submission with rating above maximum"""
    # First signup and login a user
    user_data = {"username": "testuser", "password": "testpass"}
    client.post("/auth/signup", json=user_data)
    login_response = client.post("/auth/login", json=user_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Submit feedback with invalid rating
    feedback_data = {"rating": 11, "comment": "Test comment"}
    response = client.post("/user/feedback", json=feedback_data, headers=headers)
    assert response.status_code == 422  # Validation error


def test_send_feedback_comment_too_long(client: TestClient, session: Session):
    """Test feedback submission with comment exceeding maximum length"""
    # First signup and login a user
    user_data = {"username": "testuser", "password": "testpass"}
    client.post("/auth/signup", json=user_data)
    login_response = client.post("/auth/login", json=user_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Submit feedback with comment too long (257 characters)
    long_comment = "a" * 257
    feedback_data = {"rating": 5, "comment": long_comment}
    response = client.post("/user/feedback", json=feedback_data, headers=headers)
    assert response.status_code == 422  # Validation error


def test_multiple_feedback_from_same_user(client: TestClient, session: Session):
    """Test multiple feedback submissions from the same user"""
    # First signup and login a user
    user_data = {"username": "testuser", "password": "testpass"}
    client.post("/auth/signup", json=user_data)
    login_response = client.post("/auth/login", json=user_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Submit first feedback
    feedback1 = {"rating": 5, "comment": "First feedback"}
    response1 = client.post("/user/feedback", json=feedback1, headers=headers)
    assert response1.status_code == 200
    
    # Submit second feedback
    feedback2 = {"rating": 8, "comment": "Second feedback"}
    response2 = client.post("/user/feedback", json=feedback2, headers=headers)
    assert response2.status_code == 200
    
    # Verify both feedbacks have different IDs
    feedback1_data = response1.json()
    feedback2_data = response2.json()
    assert feedback1_data["id"] != feedback2_data["id"]
    assert feedback1_data["user_id"] == feedback2_data["user_id"]  # Same user
