def test_register_and_login(client):
    # --- REGISTER ---
    register_data = {
        "username": "testuser",
        "password": "secret123",
        "email": "test@example.com"
    }
    r = client.post("/auth/register", json=register_data)
    print(r.text)
    assert r.status_code == 201
    assert r.json()["username"] == "testuser"

    # --- LOGIN ---
    login_data = {
        "username": "testuser",
        "password": "secret123"
    }
    r = client.post("/auth/login", data=login_data)
    print(r.text)
    assert r.status_code == 200
    token = r.json()["access_token"]
    assert token
