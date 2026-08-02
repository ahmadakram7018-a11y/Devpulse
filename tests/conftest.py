from doctest import testsource
import email
from click import password_option
import pytest
from fastapi.testclient import TestClient
import test
from app.main import app
from app.config import settings
from app.database import Base, SessionLocal, get_db
from sqlalchemy import create_engine, false , text
from sqlalchemy.orm import sessionmaker


from app.models import user


test_engine = create_engine(settings.TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(
    autoflush= False,
    autocommit = False,
    bind = test_engine
)

def overide_get_db():
    db =  TestSessionLocal()
    try :
        yield db
    finally:
        db.close()    


app.dependency_overrides[get_db] = overide_get_db

@pytest.fixture(scope="session" , autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind = test_engine)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_user(client):
    user_data = {
        "email": "testuser@gmail.com",
        "username": "testuser",
        "password": "testpassword123"
    }
    response = client.post("/users",json =user_data)
    assert response.status_code == 201

    return {**response.json(), "password": "testpassword123"}


@pytest.fixture
def test_user2(client):
    user_data = {
        "email": "testuser2@gmail.com",
        "username": "testuser2",
        "password": "testpassword123"
    }

    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    return {**response.json(), "password": "testpassword123"}

@pytest.fixture
def token(client, test_user):
    response = client.post("/users/login")
    data={
        "username": test_user["email"],
        "password": test_user["password"]
    }
    assert response.status_code == 200
    return response.json()["access_token"]

# client with Authorization header already set
@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture(autouse=True)
def clean_database():
    yield
    # runs after every test — cleans all tables
    db = TestSessionLocal()
    try:
        db.execute(text("TRUNCATE TABLE votes, comments, posts, users RESTART IDENTITY CASCADE"))
        db.commit()
    finally:
        db.close()