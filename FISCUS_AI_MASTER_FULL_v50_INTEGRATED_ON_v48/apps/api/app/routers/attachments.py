from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import json, shutil

router = APIRouter(prefix="/attachments", tags=["attachments"])

BASE = Path(__file__).resolve().parent.parent
STORE = BASE / "uploads"
DATA = BASE / "data" / "invoice_attachments.json"

STORE.mkdir(exist_ok=True, parents=True)

def _load():
    if DATA.exists():
        return json.loads(DATA.read_text(encoding="utf-8"))
    return {}

def _save(obj):
    DATA.write_text(json.dumps(obj, indent=2), encoding="utf-8")

@router.get("/{invoice_id}")
def list_attachments(invoice_id: str):
    data = _load()
    return data.get(invoice_id, [])

@router.post("/{invoice_id}")
def add_attachment(invoice_id: str, file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "image/png", "image/jpeg"]:
        raise HTTPException(400, detail="Unsupported file type")
    # Save file
    dest = STORE / file.filename
    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    # Record link
    data = _load()
    arr = data.get(invoice_id, [])
    arr.append({"filename": file.filename, "content_type": file.content_type})
    data[invoice_id] = arr
    _save(data)
    return {"ok": True, "filename": file.filename}

@router.get("/file/{filename}")
def get_file(filename: str):
    dest = STORE / filename
    if not dest.exists():
        raise HTTPException(404, detail="File not found")
    return FileResponse(dest)
