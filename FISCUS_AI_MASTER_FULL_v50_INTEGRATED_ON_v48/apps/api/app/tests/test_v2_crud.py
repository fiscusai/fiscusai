import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

HEADERS_ACC = {"X-Org":"ORG-ALPHA", "X-User-Role":"accountant"}
HEADERS_ADMIN = {"X-Org":"ORG-ALPHA", "X-User-Role":"admin"}

def test_customers_crud():
    # create
    r = client.post("/v2/customers/", headers=HEADERS_ACC, json={"id":"C-DEMO","name":"Demo","email":"d@x.com"})
    assert r.status_code in (200,201)
    # list
    r = client.get("/v2/customers/", headers=HEADERS_ACC)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    # update
    r = client.put("/v2/customers/C-DEMO", headers=HEADERS_ACC, json={"name":"DemoUp"})
    assert r.status_code == 200
    assert r.json().get("name") == "DemoUp"
    # delete (admin only)
    r = client.delete("/v2/customers/C-DEMO", headers=HEADERS_ADMIN)
    assert r.status_code == 200

def test_invoices_crud():
    # create
    r = client.post("/v2/invoices/", headers=HEADERS_ACC, json={
        "id":"INV-DEMO","number":"INV-DEMO","customer":"Aurea","date":"2025-08-09","total":100,"vat":18
    })
    assert r.status_code in (200,201)
    # list
    r = client.get("/v2/invoices/", headers=HEADERS_ACC)
    assert r.status_code == 200
    # update
    r = client.put("/v2/invoices/INV-DEMO", headers=HEADERS_ACC, json={"total":150})
    assert r.status_code == 200
    assert r.json().get("total") == 150
    # delete (admin)
    r = client.delete("/v2/invoices/INV-DEMO", headers=HEADERS_ADMIN)
    assert r.status_code == 200
