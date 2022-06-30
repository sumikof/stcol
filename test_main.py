from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_get_domstock_rate():
    request = {
        "symbols": ['8411.T', ],
        "date": "=20220601"
    }
    response = client.get("/rate/domstock", json=request)
    assert response.status_code == 200
    res = response.json()
    assert len(res["item"]) == 1
    assert res["item"]["8411.T"]["symbol"] == "8411.T"
    assert res["item"]["8411.T"]["rates"]["20220601"]["Close"] == 1546.0


def test_get_domstock_rate_multi_symbol():
    request = {
        "symbols": ['8411.T', '8316.T'],
        "date": "=20220601"
    }
    response = client.get("/rate/domstock", json=request)
    assert response.status_code == 200
    res = response.json()
    assert len(res["item"]) == 2
    assert res["item"]["8316.T"]["symbol"] == "8316.T"
    assert res["item"]["8316.T"]["rates"]["20220601"]["Close"] == 4001.0


def test_get_domstock_rate_multi_date():
    request = {
        "symbols": ['8411.T'],
        "date": "<20030315"
    }
    response = client.get("/rate/domstock", json=request)
    assert response.status_code == 200
    res = response.json()
    assert len(res["item"]) == 1
    assert len(res["item"]["8411.T"]["rates"]) == 3
    assert res["item"]["8411.T"]["symbol"] == "8411.T"
    assert res["item"]["8411.T"]["rates"]["20030313"]["Close"] == 1120.0


def test_get_domstock_rate_none_symbol():
    request = {
        "date": "=20220601"
    }
    response = client.get("/rate/domstock", json=request)
    assert response.status_code == 200
    res = response.json()
    assert len(res["item"]) == 3712
    assert len(res["item"]["8411.T"]["rates"]) == 1
