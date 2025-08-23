import os
import socket
from typing import Dict

def check_tcp(host: str, port: int, timeout: float = 1.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

def health_snapshot() -> Dict[str, str]:
    # Versiyon ve basit port kontrolleri
    version = os.getenv("APP_VERSION", "0.1.0")
    # DB URL parse (postgresql+psycopg2://user:pass@host:port/db)
    db_ok = "unknown"
    try:
        db_url = os.getenv("DATABASE_URL", "")
        host = "localhost"; port = 5432
        if "@" in db_url:
            after_at = db_url.split("@", 1)[1]
            hostport = after_at.split("/", 1)[0]
            if ":" in hostport:
                host, port = hostport.split(":")[0], int(hostport.split(":")[1])
            else:
                host = hostport
        db_ok = "up" if check_tcp(host, int(port)) else "down"
    except Exception:
        db_ok = "error"

    # MinIO / S3 endpoint (http://host:9000)
    s3_ok = "unknown"
    try:
        s3_endpoint = os.getenv("S3_ENDPOINT", "http://localhost:9000")
        hp = s3_endpoint.replace("http://", "").replace("https://", "").split("/")[0]
        host = hp.split(":")[0]
        port = int(hp.split(":")[1]) if ":" in hp else 9000
        s3_ok = "up" if check_tcp(host, port) else "down"
    except Exception:
        s3_ok = "error"

    # Redis
    redis_ok = "unknown"
    try:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        hp = redis_url.split("://",1)[1]
        hostport = hp.split("/",1)[0]
        host = hostport.split(":")[0]
        port = int(hostport.split(":")[1]) if ":" in hostport else 6379
        redis_ok = "up" if check_tcp(host, port) else "down"
    except Exception:
        redis_ok = "error"

    return {
        "version": version,
        "db": db_ok,
        "s3": s3_ok,
        "redis": redis_ok,
    }