from distutils.util import strtobool
import pathlib

from pydantic_settings import BaseSettings
import environ

BASE_DIR = pathlib.Path(__file__).parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')


class Settings(BaseSettings):
    debug: bool = env('DEBUG', cast=strtobool, default=False)
    
    
settings = Settings()
print(settings.debug, BASE_DIR)