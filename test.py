import pytest
import requests

def test_ping_pong(client):
    response = client.get('/')
    assert response.data.decode('utf-8') == 'Pong', "Не корректное подключение"
    assert response.status_code == 200, "Неверный код ответа"    