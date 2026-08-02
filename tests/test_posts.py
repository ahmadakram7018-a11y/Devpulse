import pytest

# ─── Get Posts Tests ───

def test_get_all_posts(client):
    response = client.get("/posts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_post_not_found(client):
    response = client.get("/posts/999")
    assert response.status_code == 404

# ─── Create Post Tests ───

def test_create_post(authorized_client):
    response = authorized_client.post("/posts/", json={
        "title": "Test Post",
        "content": "Test Content",
        "is_published": True
    })
    assert response.status_code == 201
    data = response.json()
    assert data["Post"]["title"] == "Test Post"
    assert data["votes"] == 0

def test_create_post_unauthenticated(client):
    response = client.post("/posts/", json={
        "title": "Test Post",
        "content": "Test Content"
    })
    assert response.status_code == 401

def test_create_post_missing_title(authorized_client):
    response = authorized_client.post("/posts/", json={
        "content": "Test Content"
    })
    assert response.status_code == 422

# ─── Update Post Tests ───

def test_update_own_post(authorized_client):
    # create post first
    create_response = authorized_client.post("/posts/", json={
        "title": "Original Title",
        "content": "Original Content",
        "is_published": True
    })
    assert create_response.status_code == 201
    post_id = create_response.json()["Post"]["id"]

    # update it
    response = authorized_client.put(f"/posts/{post_id}", json={
        "title": "Updated Title",
        "content": "Updated Content",
        "is_published": True
    })
    assert response.status_code == 200
    assert response.json()["Post"]["title"] == "Updated Title"

def test_update_other_users_post(authorized_client, user2_authorized_client):
    # user2 creates post
    create_response = user2_authorized_client.post("/posts/", json={
        "title": "User2 Post",
        "content": "User2 Content",
        "is_published": True
    })
    assert create_response.status_code == 201
    post_id = create_response.json()["Post"]["id"]

    # user1 tries to update
    response = authorized_client.put(f"/posts/{post_id}", json={
        "title": "Stolen Title",
        "content": "Stolen Content",
        "is_published": True
    })
    assert response.status_code == 403

def test_delete_own_post(authorized_client):
    # create post first
    create_response = authorized_client.post("/posts/", json={
        "title": "To Delete",
        "content": "Delete me",
        "is_published": True
    })
    assert create_response.status_code == 201
    post_id = create_response.json()["Post"]["id"]

    # delete it
    response = authorized_client.delete(f"/posts/{post_id}")
    assert response.status_code == 204

def test_delete_other_users_post(authorized_client, user2_authorized_client):
    # user2 creates post
    create_response = user2_authorized_client.post("/posts/", json={
        "title": "User2 Post",
        "content": "User2 Content",
        "is_published": True
    })
    assert create_response.status_code == 201
    post_id = create_response.json()["Post"]["id"]

    # user1 tries to delete
    response = authorized_client.delete(f"/posts/{post_id}")
    assert response.status_code == 403

def test_delete_non_existent_post(authorized_client):
    response = authorized_client.delete("/posts/999")
    assert response.status_code == 404

# ─── Pagination Tests ───

def test_pagination(authorized_client):
    for i in range(3):
        authorized_client.post("/posts/", json={
            "title": f"Post {i}",
            "content": f"Content {i}",
            "is_published": True
        })
    response = authorized_client.get("/posts/?limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_search(authorized_client):
    authorized_client.post("/posts/", json={
        "title": "Python Tutorial",
        "content": "Learning Python",
        "is_published": True
    })
    authorized_client.post("/posts/", json={
        "title": "FastAPI Guide",
        "content": "Learning FastAPI",
        "is_published": True
    })
    response = authorized_client.get("/posts/?search=Python")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any("Python" in item["Post"]["title"] for item in data)

    