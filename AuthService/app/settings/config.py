import nest_asyncio
from asyncio import get_event_loop, get_running_loop, new_event_loop, run, set_event_loop
from asyncpg import Pool, create_pool
import environ

import atexit

from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings



nest_asyncio.apply()

AUTH_SERVICE_DIR = Path(__file__).parent.parent
BASE_DIR = AUTH_SERVICE_DIR.parent

env = environ.Env()
environ.Env.read_env()

# print(env('POSTGRES_USER'))


class AuthJWT(BaseModel):
    private_key_path: Path = AUTH_SERVICE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = AUTH_SERVICE_DIR / 'certs' / 'jwt-public.pem'
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 14
    
    
class PostgreSQL():
    db_name: str = env('POSTGRES_DB_NAME')
    db_host: str = env('DB_HOST')
    db_port: int = env('DB_PORT')
    
    user: str = env('POSTGRES_USER')
    password: str = env('POSTGRES_PASSWORD')
    
    pool_max_size: int = 10
    pool_min_size: int = 1


class PostgreSQLPool:
    pool: Pool | None = None
    
    async def init_pool(self):
        self.pool = await create_pool(
            user=settings.postgre_sql.user,
            password=settings.postgre_sql.password,
            database=settings.postgre_sql.db_name,
            host=settings.postgre_sql.db_host,
            port=settings.postgre_sql.db_port,
            min_size=settings.postgre_sql.pool_min_size,
            max_size=settings.postgre_sql.pool_max_size
        )
    
    async def close_pool(self):
        await self.pool.close()
    
    
class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()
    postgre_sql: PostgreSQL = PostgreSQL()
    postgre_sql_pool: PostgreSQLPool = PostgreSQLPool()

    
    
# try:
settings = Settings()
    
loop = get_event_loop()
loop.run_until_complete(settings.postgre_sql_pool.init_pool())

# finally:
def clear():
    print("finally")
    try:
        loop.run_until_complete(settings.postgre_sql_pool.close_pool())
    except RuntimeError:
        print("Eventloop")
    print("finally")

atexit.register(clear)
# nj