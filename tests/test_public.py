def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.text.strip() == '"App is running"'


def test_feedback_summary_no_feedback(client):
    response = client.get("/feedback/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert data["average"] == 0


def test_feedback_summary_with_feedback(client, session):
    # Register and login a user
    user_data = {"username": "testuser", "password": "testpass"}
    client.post("/auth/signup", json=user_data)
    login_response = client.post("/auth/login", json=user_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Submit feedbacks
    feedbacks = [
        {"rating": 5, "comment": "Good"},
        {"rating": 7, "comment": "Great"},
        {"rating": 9, "comment": "Excellent"},
    ]
    for fb in feedbacks:
        resp = client.post("/user/feedback", json=fb, headers=headers)
        assert resp.status_code == 200

    # Now check summary
    response = client.get("/feedback/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 3
    assert abs(data["average"] - 7.0) < 1e-6


def test_feedback_summary_with_mixed_feedback(client, session):
    # Register and login a user
    user_data = {"username": "anotheruser", "password": "testpass"}
    client.post("/auth/signup", json=user_data)
    login_response = client.post("/auth/login", json=user_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Submit feedbacks
    feedbacks = [
        {"rating": 1, "comment": "Bad"},
        {"rating": 10, "comment": "Perfect"},
    ]
    for fb in feedbacks:
        resp = client.post("/user/feedback", json=fb, headers=headers)
        assert resp.status_code == 200

    # Now check summary
    response = client.get("/feedback/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert abs(data["average"] - 5.5) < 1e-6
