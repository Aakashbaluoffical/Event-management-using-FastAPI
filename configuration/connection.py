from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class POSTGRESDB(BaseSettings):
    USERNAME1:  str = os.environ["POSTGRES_USERNAME"]
    PASSWORD: str = os.environ["POSTGRES_PASSWORD"]
    HOST:  str = os.environ["POSTGRES_HOST"]
    PORT:  str = os.environ["POSTGRES_PORT"]
    SCHEMA: str = os.environ["POSTGRES_SCHEMA"]


class JWT_TOKEN(BaseSettings):
    SECRET_KEY:  str = os.environ["SECRET_KEY"]
    ALGORITHM: str = os.environ["ALGORITHM"]
    ACCESS_TOKEN_EXPIRE_MINUTES:  int = os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
   


class REDISCACHE(BaseSettings):
    HOST: str = os.environ["REDIS_HOST"]
    PORT:  str = os.environ["REDIS_PORT"]
    DB:  str = os.environ["REDIS_DB"]
    PASSWORD:  str = os.environ["REDIS_PASSWORD"]
    SOCKET_TIMEOUT: str = os.environ["REDIS_SOCKET_TIMEOUT"]
    

class CACHEKEY(BaseSettings):
    ALL_EVENTS: str = os.environ["CLIENT"] + os.environ["CACHE_ALL_EVENTS"]
    ALL_REGISTRATED_EVENTS : str = os.environ["CLIENT"] + os.environ["CACHE_ALL_REGISTRATED_EVENTS"]




class SETTINGS(BaseSettings):
    CACHE_EXPIRY_IN_SECONDS: int = os.environ["CLIENT"] + "_"+  os.environ["CACHE_EXPIRY_IN_SECONDS"] #SECONDS
   