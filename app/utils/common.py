from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer

from ..config import Settings
from functools import cache

@cache
def get_settings():
    return Settings()

get_bearer_token = HTTPBearer(auto_error=False)

async def get_token(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
    settings: Settings = Depends(get_settings),
) -> str:
    known_tokens = settings.api_tokens
    if auth is None or (token := auth.credentials) not in known_tokens:
        raise HTTPException(status_code=401)
    return token