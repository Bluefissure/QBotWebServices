from fastapi import APIRouter

from .image import router as router_image
from .redirect import router as router_redirect

router = APIRouter()

router.include_router(router_image, tags=["image"], prefix="/image")
router.include_router(router_redirect, tags=["redirect"], prefix="/redirect")