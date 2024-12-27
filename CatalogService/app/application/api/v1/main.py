from fastapi import FastAPI

from application.api.v1.catalog.handlers import router as catalog_router

def create_app() -> FastAPI:
    app = FastAPI(
        title='CatalogService',
        docs_url='/api/docs',
        description='Catalog service'
    )
    
    app.include_router(catalog_router, prefix='/catalog')
    return app