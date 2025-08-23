def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("ok") is True

def test_health_deep(client):
    r = client.get("/health/deep")
    assert r.status_code == 200
    body = r.json()
    assert "db" in body and "uptime" in body
