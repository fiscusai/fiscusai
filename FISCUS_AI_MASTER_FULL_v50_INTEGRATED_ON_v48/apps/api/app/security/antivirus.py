import os
from typing import Tuple, Optional

CLAMD_HOST = os.getenv("CLAMD_HOST", "127.0.0.1")
CLAMD_PORT = int(os.getenv("CLAMD_PORT", "3310"))
AV_ENABLED = os.getenv("AV_ENABLED", "true").lower() in ("1","true","yes","on")
AV_REQUIRED = os.getenv("AV_REQUIRED", "false").lower() in ("1","true","yes","on")

def scan_bytes(data: bytes) -> Tuple[bool, Optional[str]]:
    """Return (clean, signature). If AV disabled, treat as clean.
    When AV_REQUIRED and clamd not reachable, raise RuntimeError."""
    if not AV_ENABLED:
        return True, None
    try:
        import clamd
    except Exception as e:
        if AV_REQUIRED:
            raise RuntimeError("ClamAV client import failed and AV_REQUIRED is set")
        return True, None
    try:
        cd = clamd.ClamdNetworkSocket(host=CLAMD_HOST, port=CLAMD_PORT)
        # PING to ensure service is up
        try:
            cd.ping()
        except Exception:
            # Some servers don't implement PING but will answer to INSTREAM
            pass
        res = cd.instream(data)  # {'stream': ('OK', None)} or ('FOUND','Eicar-Test-Signature')
        status, sig = res.get('stream', (None, None))
        if status == 'OK':
            return True, None
        elif status == 'FOUND':
            return False, sig
        # Unknown status
        return True, None
    except Exception:
        if AV_REQUIRED:
            raise
        return True, None
