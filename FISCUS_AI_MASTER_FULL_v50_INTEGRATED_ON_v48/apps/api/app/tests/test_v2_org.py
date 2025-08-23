from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_org_required():
    r = client.get("/v2/invoices/")
    assert r.status_code == 400

def test_crud_requires_role():
    headers = {"X-Org":"ORG-ALPHA", "X-User-Role":"user"}
    r = client.post("/v2/invoices/", headers=headers, json={"number":"INV-T","customer":"X","date":"2025-08-09","total":100,"vat":18})
    assert r.status_code == 403

def test_create_list_invoice_ok():
    headers = {"X-Org":"ORG-ALPHA", "X-User-Role":"accountant"}
    r = client.post("/v2/invoices/", headers=headers, json={"number":"INV-OK","customer":"Aurea","date":"2025-08-09","total":100,"vat":18})
    assert r.status_code == 200, r.text
    r = client.get("/v2/invoices/", headers={"X-Org":"ORG-ALPHA"})
    assert any(inv["number"]=="INV-OK" for inv in r.json())
