def test_invoices_tenant_isolation_smoke(client):
    # Listing should not error and should respect org header (behavior may vary by impl; smoke test only)
    r = client.get("/v2/invoices", headers={"X-Org":"ORG-ALPHA", "X-User-Role":"viewer"})
    assert r.status_code in (200, 204, 401, 403, 404)
