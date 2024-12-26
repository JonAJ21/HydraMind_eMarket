
import asyncio
from functools import lru_cache
from punq import Container, Scope


from logic.services.recomendation import BaseRecomendationService, RESTRecomendationService
from logic.commands.recomendation import GenerateRecomendationsCommand, GenerateRecomendationsCommandHandler
from logic.queries.recomendation import GetRecomendationQuery, GetRecomendationQueryHandler
from infrastructure.models.recomendation import BaseRecomendationModel, KNNRecomendationModel
from infrastructure.repositories.recomendation import BaseRecomendationRepository, PostgreRecomendationRepository
from logic.mediator import Mediator


@lru_cache(1)
def init_container():
    return _init_container()

def _init_container() -> Container:
    container = Container()
    
    container.register(BaseRecomendationService, RESTRecomendationService, scope=Scope.singleton)
    
    container.register(GetRecomendationQueryHandler)
    container.register(GenerateRecomendationsCommandHandler)
    
    def init_mediator():
        mediator = Mediator()

        mediator.register_query(
            GetRecomendationQuery,
            [container.resolve(GetRecomendationQueryHandler)]
        )
        
        mediator.register_command(
            GenerateRecomendationsCommand,
            [container.resolve(GenerateRecomendationsCommandHandler)]
        )
        
        return mediator
    
    container.register(Mediator, factory=init_mediator)
    
    def init_recomendation_repository():
        return PostgreRecomendationRepository()
    
    container.register(BaseRecomendationRepository, factory=init_recomendation_repository, scope=Scope.singleton)
    
    def init_recomendation_model():
        model = KNNRecomendationModel(
            recomendation_repository=container.resolve(BaseRecomendationRepository)
        )
        asyncio.run(model.fit())
        return model
    
    container.register(BaseRecomendationModel, factory=init_recomendation_model, scope=Scope.singleton)
    
    return container
    