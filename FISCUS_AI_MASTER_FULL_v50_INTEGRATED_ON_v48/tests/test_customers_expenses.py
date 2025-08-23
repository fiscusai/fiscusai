import json

def test_customers_smoke(client):
    r = client.get("/customers", headers={"X-Org":"ORG-ALPHA", "X-User-Role":"viewer"})
    assert r.status_code in (200, 204, 401, 403, 404)

def test_expenses_smoke(client):
    r = client.get("/expenses", headers={"X-Org":"ORG-ALPHA", "X-User-Role":"viewer"})
    assert r.status_code in (200, 204, 401, 403, 404)
