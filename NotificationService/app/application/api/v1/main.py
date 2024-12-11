from fastapi import FastAPI

from application.api.v1.user.handlers import router as auth_router

def create_app() -> FastAPI:
    app = FastAPI(
        title='UserService',
        docs_url='/api/docs',
        description='Service for user needs'
    )
    
    app.include_router(auth_router, prefix='/user')
    return app