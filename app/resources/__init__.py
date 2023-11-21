import re
import httpx
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, Response, HTMLResponse
from app.utils.common import get_settings
from urllib.parse import unquote

settings = get_settings()
router = APIRouter()

@router.get("/redirect")
async def redirect(url: str):
    clean_url = unquote(url)
    if not any([re.match(pattern, clean_url) for pattern in settings.allowed_urls]):
        return Response(status_code=403)
    return RedirectResponse(clean_url)

@router.get("/image")
async def image(request: Request, url: str):
    clean_url = unquote(url)
    if not any([re.match(pattern, clean_url) for pattern in settings.allowed_urls]):
        return Response(status_code=403)
    async with httpx.AsyncClient() as client:
        response = await client.get(clean_url)
    print(response.status_code)
    return HTMLResponse(content=response.text, status_code=response.status_code)
