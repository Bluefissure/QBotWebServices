import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "QBotWebServices"
    root_path: str = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    file_cache_dir: str = "cache"
    allowed_urls: list = []
    api_tokens: list = []
    model_config = SettingsConfigDict(env_file=os.path.join(
        root_path, ".env"), env_file_encoding='utf-8')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cache_dir = os.path.join(self.root_path, self.file_cache_dir)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
