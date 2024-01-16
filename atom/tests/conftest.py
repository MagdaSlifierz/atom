import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from atom.models.database import Base, get_db
from atom.main import app
from atom.main import start_application

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base.metadata.create_all(bind=engine)


# Your override_get_db function here
# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()


@pytest.fixture(scope="module")
def test_app():
    # Create a test version of the app
    app = start_application()
    # app.dependency_overrides[get_db] = override_get_db

    # Pass the test app to TestClient
    client = TestClient(app)
    yield client

# @pytest.fixture(scope="module")
# def test_app():
#     client = TestClient(app)
#
#     yield client
