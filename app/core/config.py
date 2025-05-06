# app/core/config.py
import os
import sys
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = os.path.join(
            getattr(sys, '_MEIPASS', os.path.abspath(".")), ".env"
        )

settings = Settings()
