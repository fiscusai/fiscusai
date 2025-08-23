def test_live(client):
    r = client.get("/live")
    assert r.status_code in (200, 204)

def test_ready(client):
    r = client.get("/ready")
    assert r.status_code in (200, 204)
