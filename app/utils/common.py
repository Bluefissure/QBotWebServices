from ..config import Settings
from functools import cache


@cache
def get_settings():
    return Settings()
