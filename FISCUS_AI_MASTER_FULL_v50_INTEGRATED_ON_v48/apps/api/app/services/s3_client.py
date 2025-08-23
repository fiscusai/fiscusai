import os, datetime
from typing import Optional
try:
    import boto3
    from botocore.client import Config
except Exception:
    boto3 = None

S3_ENDPOINT = os.getenv("S3_ENDPOINT")
S3_REGION = os.getenv("S3_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET", "fiscus-dev")
S3_PUBLIC_BASE_URL = os.getenv("S3_PUBLIC_BASE_URL")  # e.g. https://cdn.fiscus.ai

def get_client():
    if not boto3:
        return None
    session = boto3.session.Session(
        aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
        region_name=S3_REGION,
    )
    return session.client("s3", endpoint_url=S3_ENDPOINT, config=Config(signature_version="s3v4"))

def presign_post(key: str, content_type: str, expires: int = 3600):
    client = get_client()
    if not client:
        # Fallback demo
        return {
            "url": f"{S3_ENDPOINT or 'http://localhost:9000'}/{S3_BUCKET}",
            "fields": {"key": key, "Content-Type": content_type},
            "method": "POST",
            "public_url": f"{(S3_PUBLIC_BASE_URL or (S3_ENDPOINT or 'http://localhost:9000'))}/{S3_BUCKET}/{key}"
        }
    resp = client.generate_presigned_post(
        Bucket=S3_BUCKET,
        Key=key,
        Fields={"Content-Type": content_type},
        Conditions=[["starts-with", "$Content-Type", content_type[:10]]],
        ExpiresIn=expires
    )
    public = f"{S3_PUBLIC_BASE_URL.rstrip('/')}/{key}" if S3_PUBLIC_BASE_URL else f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{key}"
    resp["method"] = "POST"
    resp["public_url"] = public
    return resp

def presign_get(key: str, expires: int = 3600) -> Optional[str]:
    client = get_client()
    if not client:
        return f"{(S3_PUBLIC_BASE_URL or (S3_ENDPOINT or 'http://localhost:9000'))}/{S3_BUCKET}/{key}"
    return client.generate_presigned_url("get_object", Params={"Bucket": S3_BUCKET, "Key": key}, ExpiresIn=expires)
