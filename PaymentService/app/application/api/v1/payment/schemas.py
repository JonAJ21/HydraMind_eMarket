
from pydantic import BaseModel

class GetPaymentStatusResponseSchema(BaseModel):
    payment_status: str
    
    @classmethod
    def from_entity(cls, payment_status) -> 'GetPaymentStatusResponseSchema':
        return GetPaymentStatusResponseSchema(
            payment_status=payment_status
        )

class GetPaymentStatusRequestSchema(BaseModel):
    name: str
    price: float