from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database_connected"] is True
    assert data["tables_found"] == 10

def test_api_dashboard_summary():
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["is_empty_database"] is False
    assert data["metrics"]["total_revenue"] > 0
    assert data["metrics"]["completed_orders"] > 0

def test_api_products():
    response = client.get("/api/products")
    assert response.status_code == 200
    prods = response.json()
    assert len(prods) >= 30

def test_api_customers():
    response = client.get("/api/customers?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 100
    assert len(data["customers"]) == 10

def test_api_orders():
    response = client.get("/api/orders?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 500
    assert len(data["orders"]) == 10

def test_api_suppliers():
    response = client.get("/api/suppliers")
    assert response.status_code == 200
    sups = response.json()
    assert len(sups) >= 10

def test_api_inventory():
    response = client.get("/api/inventory")
    assert response.status_code == 200
    inv = response.json()
    assert len(inv) >= 30

def test_api_algorithms_run():
    payload = {
        "algorithm_name": "Merge Sort",
        "input_size": 50,
        "iterations": 2
    }
    response = client.post("/api/algorithms/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["algorithm_name"] == "Merge Sort"
    assert data["input_size"] == 50
    assert data["median_time_ms"] >= 0
    assert data["persisted"] is True
