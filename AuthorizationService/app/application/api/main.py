from fastapi import FastAPI

# from common.settings import settings

def create_app():
    return FastAPI(
        title='AuthorizationService',
        docs_url='/api/docs',
        description='Service for authorization'
        # debug=settings.debug,
    )