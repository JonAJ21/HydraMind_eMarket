
import environ
from pydantic_settings import BaseSettings

import nest_asyncio

nest_asyncio.apply()

env = environ.Env()
environ.Env.read_env()
 
class Settings(BaseSettings):
    token: str = env('TOKEN')
    receiver: str = env('RECEIVER')
    
settings = Settings()