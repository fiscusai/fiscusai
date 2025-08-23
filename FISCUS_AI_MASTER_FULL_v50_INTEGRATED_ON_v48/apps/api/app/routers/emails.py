from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path

router = APIRouter(prefix="/emails", tags=["emails"])

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"
env = Environment(
    loader=FileSystemLoader(str(TEMPLATES)),
    autoescape=select_autoescape()
)

@router.get("/welcome-preview", response_class=HTMLResponse)
def welcome_preview():
    tpl = env.get_template("emails/welcome.html")
    html = tpl.render(verify_url="https://fiscus.ai/verify?code=DEMO-CODE")
    return HTMLResponse(content=html)
