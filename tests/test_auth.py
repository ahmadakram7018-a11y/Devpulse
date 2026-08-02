# ─── User Registration Tests ───
from fastapi.testclient import TestClient
import pytest

from tests.conftest import clean_database

def test_register_user(client):
    """New user can register successfully"""
    response = client.post("/users/", json={
        "email": "newuser@gmail.com",
        "username": "newuser",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@gmail.com"
    assert data["username"] == "newuser"
    assert "password" not in data  # password never exposed
    

def test_register_missing_fields(client):
    """Registration fails when required fields missing"""
    response = client.post("/users/", json={
        "email": "incomplete@gmail.com"
        # missing username and password
    })
    assert response.status_code == 422  # validation error
    

# ─── Login Tests ───

def test_login_success(client, test_user):
    """User can login with correct credentials"""
    response = client.post("/auth/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    

def test_login_wrong_password(client, test_user):
    """Login fails with wrong password"""
    response = client.post("/auth/login", data={
        "username": test_user["email"],
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    

def test_login_wrong_email(client):
    """Login fails with non-existent email"""
    response = client.post("/auth/login", data={
        "username": "nobody@gmail.com",
        "password": "password123"
    })
    assert response.status_code == 401
    

def test_login_missing_password(client, test_user):
        response = client.post("/auth/login", data={
        "username": test_user["email"]
    })
        assert response.status_code == 422
    

