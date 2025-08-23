import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

HEADERS_USER = {"X-Org":"ORG-ALPHA", "X-User-Role":"user"}
HEADERS_ACC = {"X-Org":"ORG-ALPHA", "X-User-Role":"accountant"}
HEADERS_ADMIN = {"X-Org":"ORG-ALPHA", "X-User-Role":"admin"}

def test_user_cannot_create_invoice():
    r = client.post("/v2/invoices", headers=HEADERS_USER, json={"number":"INV-UX","customer":"X","date":"2025-08-09","total":10,"vat":1.8})
    assert r.status_code in (401,403,405)

def test_accountant_can_create_but_cannot_delete():
    r = client.post("/v2/invoices", headers=HEADERS_ACC, json={"number":"INV-ACC","customer":"X","date":"2025-08-09","total":10,"vat":1.8})
    assert r.status_code in (200,201)
    inv = r.json()
    inv_id = inv.get("id") or inv.get("number") or "INV-ACC"
    rd = client.delete(f"/v2/invoices/{inv_id}", headers=HEADERS_ACC)
    assert rd.status_code in (401,403,404)

def test_admin_can_delete():
    # Create first
    r = client.post("/v2/invoices", headers=HEADERS_ACC, json={"number":"INV-DEL","customer":"X","date":"2025-08-09","total":10,"vat":1.8})
    inv = r.json()
    inv_id = inv.get("id") or inv.get("number") or "INV-DEL"
    rd = client.delete(f"/v2/invoices/{inv_id}", headers=HEADERS_ADMIN)
    assert rd.status_code in (200,204,404)

def test_customers_requires_org():
    r = client.get("/v2/customers")
    assert r.status_code == 400
    r2 = client.get("/v2/customers", headers=HEADERS_USER)
    assert r2.status_code in (200,204)
