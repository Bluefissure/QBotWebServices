import re
from urllib.parse import unquote
import httpx
import os
import io
import base64
from PIL import Image
from hashlib import sha256
from pydantic import BaseModel

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse, Response, StreamingResponse
from app.utils.common import get_settings, get_token
from ..config import Settings

router = APIRouter()

@router.get("/")
async def image(
        url: str = None,
        file: str = None,
        settings: Settings = Depends(get_settings),
        response_class=Response,
    ):
    if url:
        clean_url = unquote(url)
        if not any([re.match(pattern, clean_url) for pattern in settings.allowed_urls]):
            raise HTTPException(status_code=403)
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        return StreamingResponse(response.iter_bytes(), media_type=response.headers['Content-Type'])
    elif file:
        cache_dir = settings.file_cache_dir
        file_on_disk = os.path.join(cache_dir, file)
        if not os.path.exists(file_on_disk):
            raise HTTPException(status_code=404)
        with open(file_on_disk, "rb") as f:
            image_bytes = f.read()
        ext = file.split('.')[-1]
        return Response(content=image_bytes, media_type=f"image/{ext}")
    raise HTTPException(status_code=400)


class B64Image(BaseModel):
    base64: str
    

@router.post("/")
async def post_image(
        image: B64Image,
        token: str = Depends(get_token),
        settings: Settings = Depends(get_settings),
    ):
    b64str = image.base64.strip()
    filext = 'png'
    ext_pattern = r'data:image/(.+);base64,'
    s = re.search(ext_pattern, b64str)
    if s:
        filext = s.group(1)
        b64str = re.sub(ext_pattern, '', b64str)
    cache_dir = settings.file_cache_dir
    cache_file_hash = sha256(b64str.encode()).hexdigest()
    cache_file = cache_file_hash + '.' + filext
    cache_file_path = os.path.join(cache_dir, cache_file)
    img = Image.open(io.BytesIO(base64.decodebytes(bytes(b64str, "utf-8"))))
    img.save(cache_file_path)
    return {
        "file": cache_file,
    }

