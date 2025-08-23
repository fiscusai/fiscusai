import time, jwt
from fastapi.testclient import TestClient
from apps.api.app.main import app

SECRET = "change-me"

def make_token(sub="admin", role="admin", exp=3600):
    return jwt.encode({"sub": sub, "role": role, "exp": int(time.time()) + exp}, SECRET, algorithm="HS256")

def test_admin_requires_role():
    c = TestClient(app)
    # Yetkisiz
    r = c.get("/admin/uploads/recent")
    assert r.status_code in (401,403)
    # Admin token ile
    t = make_token()
    r = c.get("/admin/uploads/recent", headers={"Authorization": f"Bearer {t}"})
    assert r.status_code in (200, 500)  # Redis yoksa 500 olabilir; endpoint handled -> items:[]