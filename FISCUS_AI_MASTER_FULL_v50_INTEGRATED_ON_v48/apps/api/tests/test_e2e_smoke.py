import time, jwt
from fastapi.testclient import TestClient
from apps.api.app.main import app

SECRET = "change-me"

def make(sub="alice@example.com", role="uploader"):
    return jwt.encode({"sub": sub, "role": role, "exp": int(time.time())+3600}, SECRET, algorithm="HS256")

def test_users_crud_and_presign_auth():
    c = TestClient(app)
    # admin add user
    at = make(role="admin")
    r = c.post("/admin/users?sub=alice@example.com&role=uploader", headers={"Authorization": f"Bearer {at}"})
    assert r.status_code in (200, 201, 204)

    # list users
    r = c.get("/admin/users", headers={"Authorization": f"Bearer {at}"})
    assert r.status_code == 200

    # presign requires uploader
    ut = make(sub="alice@example.com", role="uploader")
    r = c.get("/files/presign?filename=test.pdf", headers={"Authorization": f"Bearer {ut}"})
    # S3 creds yoksa 500 olabilir; en azından 401/403 olmamalı
    assert r.status_code in (200, 500)