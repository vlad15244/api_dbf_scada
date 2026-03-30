import pytest
import requests

from server import app

@pytest.fixture
def client():
    """Создаёт тестовый клиент."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client