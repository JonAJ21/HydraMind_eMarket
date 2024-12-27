from abc import ABC, abstractmethod
from dataclasses import dataclass

from yoomoney import Client
from yoomoney import Quickpay


from settings.config import settings


@dataclass
class BasePaymentService(ABC):
    
    @abstractmethod
    async def get_payment_status(self, name: str, price: int) -> str:
        ...
    
    
@dataclass
class YoomoneyPaymenService(BasePaymentService):
    
    async def get_payment_status(self, name: str, price: int) -> str:
        quickpay = Quickpay(
            receiver=settings.receiver,
            quickpay_form="shop",
            targets=name,
            paymentType="SB",
            sum=price,
            label="a1b2c3d4e5"
            )
        print(quickpay.base_url)
        client = Client(settings.token)
        history = client.operation_history(label="a1b2c3d4e5")
        for operation in history.operations:
            if operation.operation_id == 'success':
                return 'success'
        return 'success'