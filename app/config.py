import os
import json

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "QBotWebServices"
    root_path: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_cache_dir: str = "cache"
    allowed_urls: list = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cache_dir = os.path.join(self.root_path, self.file_cache_dir)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
