from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter(tags=["Project"])
GREETING_FILE = Path(__file__).resolve().parents[1] / "greeting.html"


@router.get("/greeting", response_class=HTMLResponse)
async def greeting():
    return HTMLResponse(GREETING_FILE.read_text(encoding="utf-8"))
