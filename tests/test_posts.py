def test_create_list_delete_post(client):
    # --- LOGIN ---
    login = client.post("/auth/login", data={"username": "testuser", "password": "secret123"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # --- CREATE POST ---
    post_data = {"url": "https://example.com/article"}
    r = client.post("/posts/", json=post_data, headers=headers)
    print(r.text)
    assert r.status_code == 201
    post = r.json()
    assert post["url"] == "https://example.com/article"

    # --- LIST POSTS ---
    r = client.get("/posts/", headers=headers)
    print(r.text)
    assert r.status_code == 200
    posts = r.json()
    assert len(posts) >= 1

    # --- DELETE POST ---
    post_id = post["id"]
    r = client.delete(f"/posts/{post_id}", headers=headers)
    print(r.text)
    assert r.status_code == 204
