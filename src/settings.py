from decouple import config
from pydantic import BaseSettings


#class ServiceSettings(BaseSettings):
ENV_SERVER = config("ENV_SERVER", default="LOCAL")
APPLICATION_NAME = config("APPLICATION_NAME", default='hexagonal-architecture-with-python')
PORT = config("PORT", default=8000, cast=int)
UVICORN_WORKERS = config("UVICORN_WORKERS", default=3, cast=int)
ACCEPT_PARALLEL_REQUESTS = config(
    "ACCEPT_PARALLEL_REQUESTS",
    default=False,
    cast=bool
)
USE_DATABASE = config("USE_DATABASE", default=False, cast=bool)


#class RedisSettings(BaseSettings):
REDIS_HOST = config("REDIS_HOST", default="redis")
REDIS_PORT = config("REDIS_PORT", default=6379, cast=int)
REDIS_PASSWORD = config("REDIS_PASSWORD", default=None)
REDIS_SSL = config("REDIS_SSL", default=False, cast=bool)
CACHE_SILENT_MODE = config("CACHE_SILENT_MODE", default=True, cast=bool)

USE_DATABASE = config("USE_DATABASE", default=False, cast=bool)
if USE_DATABASE:
    #class DatabaseSettings(BaseSettings):
    DB_PROVIDER = config('DB_PROVIDER')
    DB_USER = config('DB_USER')
    DB_PASSWORD = config('DB_PASSWORD')
    DB_HOST = config('DB_HOST')
    DB_NAME = config('DB_NAME')
    DB_URL = f"{DB_PROVIDER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
else:
    DATABASE_URL = "sqlite:///db.sqlite"

class MongoDatabaseSettings(BaseSettings):
    MONGO_SERVER: str = config("MONGO_SERVER", default="event-source-mongo-db")
    MONGO_PORT: str = config("MONGO_PORT", default="27017")
    MONGO_USERNAME: str = config("MONGO_USERNAME", default="root")
    MONGO_PASSWORD: str = config("MONGO_PASSWORD", default="admin")

class MongoDatabaseSettings(BaseSettings):
    MONGO_SERVER: str = 'mongo-db'
    MONGO_PORT: str = '27017'
    MONGO_USERNAME: str = ''
    MONGO_PASSWORD: str = ''