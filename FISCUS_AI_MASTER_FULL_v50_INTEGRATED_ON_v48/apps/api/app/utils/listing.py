
from __future__ import annotations
from typing import List, Dict, Any, Tuple, Optional
import hashlib, json as _json
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone

def apply_query_sort(items: List[Dict[str, Any]], q: Optional[str] = None, sort: Optional[str] = None) -> List[Dict[str, Any]]:
    data = items
    if q:
        ql = q.lower()
        def matches(obj):
            for v in obj.values():
                try:
                    s = f"{v}".lower()
                    if ql in s:
                        return True
                except Exception:
                    continue
            return False
        data = [it for it in data if matches(it)]
    if sort:
        # sort format: field or field:asc|desc
        parts = (sort or "").split(":")
        field = parts[0]
        order = (parts[1] if len(parts) > 1 else "asc").lower()
        reverse = order == "desc"
        def keyf(x):
            try:
                return x.get(field, "")
            except Exception:
                return ""
        try:
            data = sorted(data, key=keyf, reverse=reverse)
        except Exception:
            pass
    return data

def paginate(items: List[Dict[str, Any]], page: int, page_size: int) -> Tuple[List[Dict[str, Any]], int]:
    page = max(1, int(page or 1))
    page_size = max(1, min(200, int(page_size or 20)))
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    return items[start:end], total

def make_etag(payload) -> str:
    try:
        body = _json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    except Exception:
        body = str(payload).encode("utf-8")
    return hashlib.sha256(body).hexdigest()

def set_cache_headers(request, response, payload, last_modified: Optional[datetime] = None):
    # ETag
    etag = make_etag(payload)
    response.headers['X-ETag'] = etag
    inm = request.headers.get("If-None-Match")
    if inm and inm == etag:
        response.status_code = 304
        return True

    # Last-Modified
    if last_modified:
        if last_modified.tzinfo is None:
            last_modified = last_modified.replace(tzinfo=timezone.utc)
        response.headers["Last-Modified"] = last_modified.strftime("%a, %d %b %Y %H:%M:%S GMT")
        ims = request.headers.get("If-Modified-Since")
        if ims:
            try:
                ims_dt = parsedate_to_datetime(ims)
                if ims_dt.tzinfo is None:
                    ims_dt = ims_dt.replace(tzinfo=timezone.utc)
                if last_modified <= ims_dt:
                    response.status_code = 304
                    return True
            except Exception:
                pass
    return False
