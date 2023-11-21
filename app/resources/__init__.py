import re
from urllib.parse import unquote
import httpx
from fastapi import APIRouter
from fastapi.responses import RedirectResponse, Response, StreamingResponse
from app.utils.common import get_settings

settings = get_settings()
router = APIRouter()


@router.get("/redirect")
async def redirect(url: str):
    clean_url = unquote(url)
    if not any([re.match(pattern, clean_url) for pattern in settings.allowed_urls]):
        return Response(status_code=403)
    return RedirectResponse(clean_url)


@router.get("/image")
async def image(url: str):
    clean_url = unquote(url)
    if not any([re.match(pattern, clean_url) for pattern in settings.allowed_urls]):
        return Response(status_code=403)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return StreamingResponse(response.iter_bytes(), media_type=response.headers['Content-Type'])
