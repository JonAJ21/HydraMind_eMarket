from asyncio import get_event_loop
import atexit
from asyncpg import Pool, create_pool
import environ
from pydantic_settings import BaseSettings

import nest_asyncio

nest_asyncio.apply()

env = environ.Env()
environ.Env.read_env()


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
        
class Services():
    auth: str = str(env('AUTH_SERVICE_URL')) + '/auth'

 
class Settings(BaseSettings):
    postgre_sql: PostgreSQL = PostgreSQL()
    postgre_sql_pool: PostgreSQLPool = PostgreSQLPool()
    services: Services = Services()
    
settings = Settings()

loop = get_event_loop()
loop.run_until_complete(settings.postgre_sql_pool.init_pool())

def clear():
    print("finally")
    try:
        loop.run_until_complete(settings.postgre_sql_pool.close_pool())
    except RuntimeError:
        print("Eventloop")
    print("finally")

atexit.register(clear)