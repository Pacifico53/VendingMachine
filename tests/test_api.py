import pytest
from main import app


@pytest.fixture
def client():
    """Fixture to set up the test client."""
    app.testing = True
    return app.test_client()


def test_get_products(client):
    response = client.get("/api/products")
    assert response.status_code == 200
    data = response.get_json()
    assert "chips" in data
    assert data["chips"]["price"] == 70


def test_purchase_success(client):
    response = client.post("/api/purchase", json={
        "product": "chips",
        "payment": [100]
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Purchase successful"
    assert data["product"] == "chips"
    assert data["change_dispensed"] == 30


def test_purchase_insufficient_funds(client):
    response = client.post("/api/purchase", json={
        "product": "chips",
        "payment": [50]
    })
    assert response.status_code == 402
    data = response.get_json()
    assert "Insufficient funds" in data["error"]


def test_reload_machine(client):
    response = client.post("/api/reload", json={
        "coins": {10: 5},
        "products": {"chips": 2}
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Machine reloaded successfully."


def test_warn_low_coins(client):
    response = client.get("/api/warn-low-coins")
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data or "warning" in data
