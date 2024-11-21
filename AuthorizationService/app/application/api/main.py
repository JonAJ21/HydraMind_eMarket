from fastapi import FastAPI

from application.api.user.handlers import router as message_router


def create_app() -> FastAPI:
    app = FastAPI(
        title='AuthorizationService',
        docs_url='/api/docs',
        description='Service for authorization'
    )
    
    app.include_router(message_router, prefix='/chat')
    
    return app