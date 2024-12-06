from fastapi import FastAPI

from application.api.v1.gateway.user import router as user_router
from application.api.v1.gateway.auth import router as auth_router

def create_app() -> FastAPI:
    app = FastAPI(
        title='Gateway',
        docs_url='/api/docs',
        description='Gateway'
    )    
    app.include_router(auth_router, prefix='/auth')
    app.include_router(user_router, prefix='/user')
    
    return app