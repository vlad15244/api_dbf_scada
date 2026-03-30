import pytest
import requests

from server import app

@pytest.fixture
def client():
    """Создаёт тестовый клиент."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_dbf_table(mocker):
    """Мокирует работу с DBF‑таблицей."""
    mock_table = mocker.MagicMock()
    mock_table.field_names = ['ID', 'VALUE']
    mock_table.__enter__ = mocker.Mock(return_value=mock_table)
    mock_table.__exit__ = mocker.Mock()
    return mock_table