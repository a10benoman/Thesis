import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, engine


@pytest.fixture
def client():
    """Provide a test client with database initialized."""
    # Create all tables before the test
    Base.metadata.create_all(bind=engine)
    
    client = TestClient(app)
    
    yield client
    
    # Clean up after test
    Base.metadata.drop_all(bind=engine)
