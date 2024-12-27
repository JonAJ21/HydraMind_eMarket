from fastapi import FastAPI

from application.api.v1.notification.handlers import router as notification_router

def create_app() -> FastAPI:
    app = FastAPI(
        title='NotificationService',
        docs_url='/api/docs',
        description='Notification service'
    )
    
    app.include_router(notification_router, prefix='/notification')
    return app