
from fastapi import APIRouter
import httpx
from settings.config import services


router = APIRouter(
    tags=['user-service']
    
)

@router.get(
    '/hello'
)
async def get_test():
    
    async with httpx.AsyncClient() as client:
        url = f"{services['user']}{'/hello'}"
        response = await client.request('GET', url, json=None, headers=None)
    return response.json()


# async def forward_request(service_url: str, method: str, path: str, body=None, headers=None):
#     async with httpx.AsyncClient() as client:
#         url = f"{service_url}{path}"
#         response = await client.request(method, url, json=body, headers=headers)
#         return response
    
# @router.api_route(
#     "/{service}/{path:path}",
#     methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
# )
# async def gateway(service: str, path: str, request: Request):
#     if service not in services:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Service not found')
    
#     service_url = services[service]
#     body = await request.json() if request.method in  ['POST', 'PUT', 'PATCH'] else None
#     headers = dict(request.headers)
    
#     response = await forward_request(service_url, request.method, f"{path}", body, headers)
    
#     return JSONResponse(status_code=response.status_code, content=response.json())