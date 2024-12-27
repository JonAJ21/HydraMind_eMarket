
from functools import lru_cache
from punq import Container, Scope

from logic.queries.payment import GetPaymentStatusQueryHandler, GetPaymentStatusQuery
from logic.services.payment import BasePaymentService, YoomoneyPaymenService
from logic.mediator import Mediator


@lru_cache(1)
def init_container():
    return _init_container()

def _init_container() -> Container:
    container = Container()
    
    container.register(BasePaymentService, YoomoneyPaymenService, scope=Scope.singleton)
    
    container.register(GetPaymentStatusQueryHandler)
    
    
    def init_mediator():
        mediator = Mediator()
        
        mediator.register_query(
            GetPaymentStatusQuery,
            [container.resolve(GetPaymentStatusQueryHandler)]
        )
        
        return mediator
    
    container.register(Mediator, factory=init_mediator)
    
    return container
    
