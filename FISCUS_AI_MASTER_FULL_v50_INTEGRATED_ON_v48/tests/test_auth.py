import uuid, json

def test_register_login_refresh(client):
    email = f"demo+{uuid.uuid4().hex[:6]}@firm.com"
    # register
    r = client.post("/auth/register", json={"email": email, "password": "Sifre!2025", "org":"ORG-TEST"})
    assert r.status_code in (200, 201, 204), r.text

    # login
    r = client.post("/auth/login", json={"email": email, "password": "Sifre!2025"})
    assert r.status_code == 200, r.text
    data = r.json()
    assert "access_token" in data
    assert "refresh_token" in data

    # refresh
    r2 = client.post("/auth/refresh", json={"refresh_token": data["refresh_token"]})
    assert r2.status_code == 200, r2.text
    assert "access_token" in r2.json()
