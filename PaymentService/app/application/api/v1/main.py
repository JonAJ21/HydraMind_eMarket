from fastapi import FastAPI

from application.api.v1.payment.handlers import router as payment_router

def create_app() -> FastAPI:
    app = FastAPI(
        title='PaymentService',
        docs_url='/api/docs',
        description='Notification service'
    )
    
    app.include_router(payment_router, prefix='/payment')
    return app