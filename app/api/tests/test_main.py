from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_healthcheck():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_market_overview():
    response = client.get('/api/v1/market/overview')
    assert response.status_code == 200
    data = response.json()
    assert 'market_status' in data
    assert 'indices' in data


def test_market_signals():
    response = client.get('/api/v1/market/signals')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert 'symbol' in data[0]
