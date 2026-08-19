import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.config import settings

# test database setup
test_engine = create_engine(settings.TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

# create tables once for entire test session
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

# fresh db session for every test — rolls back after
@pytest.fixture()
def db():
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

# plain client — no auth
@pytest.fixture()
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

# test user 1
@pytest.fixture()
def test_user(client):
    response = client.post("/users/", json={
        "email": "testuser@gmail.com",
        "username": "testuser",
        "password": "testpassword123"
    })
    assert response.status_code == 201
    return {**response.json(), "password": "testpassword123"}

# test user 2
@pytest.fixture()
def test_user2(client):
    response = client.post("/users/", json={
        "email": "testuser2@gmail.com",
        "username": "testuser2",
        "password": "testpassword123"
    })
    assert response.status_code == 201
    return {**response.json(), "password": "testpassword123"}

# token for user 1
@pytest.fixture()
def token(client, test_user):
    response = client.post("/auth/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    return response.json()["access_token"]

# authenticated client for user 1 — separate instance
@pytest.fixture()
def authorized_client(db, token):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        c.headers = {**c.headers, "Authorization": f"Bearer {token}"}
        yield c
    app.dependency_overrides.clear()

# authenticated client for user 2 — separate instance
@pytest.fixture()
def user2_authorized_client(db, client, test_user2):
    login_response = client.post("/auth/login", data={
        "username": test_user2["email"],
        "password": test_user2["password"]
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        c.headers = {**c.headers, "Authorization": f"Bearer {token}"}
        yield c
    app.dependency_overrides.clear()





    