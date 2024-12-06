
from fastapi import APIRouter


router = APIRouter(
    tags=['User']
    
)

@router.get(
    '/hello'
)
async def get_hello():
    return {'message': 'hello'}