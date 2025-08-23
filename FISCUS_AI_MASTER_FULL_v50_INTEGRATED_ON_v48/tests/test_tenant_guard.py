import pytest
from fastapi import Depends, HTTPException
from apps.api.app.security.deps import get_org

def test_get_org_sets_state(monkeypatch):
    class DummyReq:
        state = type("obj", (), {})()
        headers = {"x-org": "demo-org"}
    req = DummyReq()
    org = get_org(req)
    assert org == "demo-org"
