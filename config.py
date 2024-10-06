from environs import Env
from dataclasses import dataclass


env = Env()
env.read_env()


class Settings():
    DB_HOST: str = env('DB_HOST')
    DB_PORT: int = env('DB_PORT')
    DB_USER: str = env('DB_USER')
    DB_PASS: str = env('DB_PASS')
    DB_NAME: str = env('DB_NAME')
    
    BOT_TOKEN: str = env('BOT_TOKEN')
        
settings = Settings()


DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
