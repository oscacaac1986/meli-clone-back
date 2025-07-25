import asyncio

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def client():
    """Create a test client"""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def sample_product_data():
    """Sample product data for testing"""
    return {
        "id": "MLA123456789",
        "title": "Samsung Galaxy A55 5G Test",
        "price": 439,
        "currency": "US$",
        "condition": "Nuevo",
        "seller_id": "SELLER001"
    }