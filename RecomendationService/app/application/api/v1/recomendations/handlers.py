from fastapi import APIRouter, Depends, HTTPException, status

from logic.commands.recomendation import GenerateRecomendationsCommand
from domain.exceptions.base import ApplicationException
from logic.queries.recomendation import GetRecomendationQuery
from logic.mediator import Mediator
from logic.init import init_container
from application.api.v1.recomendations.schemas import GenerateRecomendationsRequestScheme, GenerateRecomendationsResponseScheme, GetRecomendationRequestScheme, GetRecomendationsResponseScheme
from application.api.v1.schemas import ErrorSchema

router = APIRouter(
    tags=['recomendations']    
)

@router.post(
    '/generate/recomendations',
    response_model=GenerateRecomendationsResponseScheme,
    status_code=status.HTTP_201_CREATED,
    description='Generate recomendations',
    responses={
       status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def generate_recomendations_handler(
    scheme: GenerateRecomendationsRequestScheme, 
    container=Depends(init_container)
):
    '''Generate recomendations'''
    mediator: Mediator = container.resolve(Mediator)
    try:
        recomendation, *_ = await mediator.handle_command(
            GenerateRecomendationsCommand(
                token=scheme.token,
                n_recommendations=scheme.n_recommendations
            )
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'error': exception.message}
        )
    print(recomendation)
    return GenerateRecomendationsResponseScheme(
        message='Recomendations generated successfully'
    )


@router.get(
    '/get/recomendations',
    response_model=GetRecomendationsResponseScheme,
    status_code=status.HTTP_200_OK,
    description='Get recomendations',
    responses={
       status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    }
)
async def get_recomendations_handler(
    scheme: GetRecomendationRequestScheme,
    container=Depends(init_container)
):
    '''Get recomendations'''
    
    mediator: Mediator = container.resolve(Mediator)
    try:
        recomendation, *_ = await mediator.handle_query(
            GetRecomendationQuery(
                token=scheme.token,
                n_recommendations=scheme.n_recommendations
            )
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'error': exception.message}
        )
        
    print("recomendation", recomendation)
    return GetRecomendationsResponseScheme.from_entity(recomendation)