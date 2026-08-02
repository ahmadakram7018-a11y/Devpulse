import pytest

@pytest.fixture()
def test_post(authorized_client):
    response = authorized_client.post("/posts/", json={
        "title": "Vote Test Post",
        "content": "Vote Test Content",
        "is_published": True
    })
    assert response.status_code == 201
    return response.json()["Post"]

# ─── Vote Tests ───

def test_vote_on_post(authorized_client, test_post):
    response = authorized_client.post("/votes/", json={
        "post_id": test_post["id"],
        "direction": 1
    })
    assert response.status_code == 201

def test_vote_twice_on_same_post(authorized_client, test_post):
    # first vote
    authorized_client.post("/votes/", json={
        "post_id": test_post["id"],
        "direction": 1
    })
    # second vote — should fail
    response = authorized_client.post("/votes/", json={
        "post_id": test_post["id"],
        "direction": 1
    })
    assert response.status_code == 409

def test_remove_vote(authorized_client, test_post):
    # vote first
    authorized_client.post("/votes/", json={
        "post_id": test_post["id"],
        "direction": 1
    })
    # remove vote
    response = authorized_client.post("/votes/", json={
        "post_id": test_post["id"],
        "direction": 0
    })
    assert response.status_code == 201

def test_remove_non_existent_vote(authorized_client, test_post):
    response = authorized_client.post("/votes/", json={
        "post_id": test_post["id"],
        "direction": 0
    })
    assert response.status_code == 404

def test_vote_unauthenticated(client, authorized_client, test_post):
    response = client.post("/votes/", json={
        "post_id": test_post["id"],
        "direction": 1
    })
    assert response.status_code == 401

def test_vote_non_existent_post(authorized_client):
    response = authorized_client.post("/votes/", json={
        "post_id": 999,
        "direction": 1
    })
    assert response.status_code == 404

def test_invalid_direction(authorized_client, test_post):
    response = authorized_client.post("/votes/", json={
        "post_id": test_post["id"],
        "direction": 5
    })
    assert response.status_code == 422