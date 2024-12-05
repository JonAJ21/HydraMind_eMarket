from fastapi import FastAPI

from application.api.v1.auth.handlers import router as auth_router

def create_app() -> FastAPI:
    app = FastAPI(
        title='AuthService',
        docs_url='/api/docs',
        description='Service for auth'
    )
    
    app.include_router(auth_router, prefix='/auth')
    return app