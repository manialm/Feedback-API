from conftest import admin_user_data

regular_user = {"username": "user", "password": "userpass"}


def get_token(client, user):
    client.post("/auth/signup", json=user)
    resp = client.post("/auth/login", json=user)
    return resp.json()["access_token"]


def get_admin_token(client, admin_user):
    # admin_user fixture ensures admin exists in DB
    resp = client.post("/auth/login", json=admin_user_data)
    return resp.json()["access_token"]


def test_admin_list_users(client, admin_user):
    # Create users
    client.post("/auth/signup", json=regular_user)
    admin_token = get_admin_token(client, admin_user)
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/admin/users", headers=headers)
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert any(u["username"] == regular_user["username"] for u in users)


def test_admin_access_denied_for_non_admin(client, admin_user):
    # Create and login as regular user
    client.post("/auth/signup", json=regular_user)
    token = get_token(client, regular_user)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/admin/users", headers=headers)
    assert response.status_code == 403 or response.status_code == 401


def test_admin_update_user(client, admin_user):
    # Create user
    client.post("/auth/signup", json=regular_user)
    admin_token = get_admin_token(client, admin_user)
    headers = {"Authorization": f"Bearer {admin_token}"}
    users = client.get("/admin/users", headers=headers).json()
    user_id = next(u["id"] for u in users if u["username"] == regular_user["username"])
    update_data = {"username": "updateduser"}
    response = client.patch(
        f"/admin/users/{user_id}", json=update_data, headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updateduser"
