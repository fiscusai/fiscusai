from app.security.antivirus import scan_bytes
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
import uuid, shutil

router = APIRouter(prefix="/uploads", tags=["uploads"])

BASE = Path(__file__).resolve().parent.parent / "uploads"
BASE.mkdir(exist_ok=True, parents=True)

ALLOWED = {"application/pdf","image/png","image/jpeg"}
MAX_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("/")
async def upload(file: UploadFile = File(...), invoice_id: str = Form(None)):
    if file.content_type not in ALLOWED:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    # stream to disk with size guard
    suffix = { "application/pdf": ".pdf", "image/png": ".png", "image/jpeg": ".jpg" }.get(file.content_type, "")
    fname = f"{invoice_id or 'misc'}_{uuid.uuid4().hex}{suffix}"
    dest = BASE / fname
    size = 0
    with dest.open("wb") as out:
        while True:
            chunk = await file.read(512 * 1024)
            if not chunk:
                break
            size += len(chunk)
            if size > MAX_SIZE:
                dest.unlink(missing_ok=True)
                raise HTTPException(status_code=413, detail="File too large (>10MB)")
            out.write(chunk)
    return {"ok": True, "filename": fname, "size": size, "invoice_id": invoice_id}

@router.get("/{filename}")
def get_file(filename: str):
    path = BASE / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    media_type = "application/octet-stream"
    if path.suffix == ".pdf":
        media_type = "application/pdf"
    elif path.suffix == ".png":
        media_type = "image/png"
    elif path.suffix == ".jpg":
        media_type = "image/jpeg"
    return FileResponse(path, media_type=media_type)
