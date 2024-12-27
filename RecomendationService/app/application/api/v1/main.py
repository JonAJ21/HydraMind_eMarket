from fastapi import FastAPI

from application.api.v1.recomendations.handlers import router as recomendations_router

def create_app() -> FastAPI:
    app = FastAPI(
        title='RecomendationService',
        docs_url='/api/docs',
        description='Recomendation service'
    )
    
    app.include_router(recomendations_router, prefix='/recomendations')
    return app
