
from fastapi import APIRouter, Depends, HTTPException, status

from logic.queries.notification import GetLimitNotificationsQuery, GetUnreadNotificationsQuery
from logic.commands.notification import AddNotificationCommand
from domain.exceptions.base import ApplicationException
from logic.mediator import Mediator
from logic.init import init_container
from application.api.v1.schemas import ErrorSchema
from application.api.v1.notification.schemas import AddNotificationRequestSchema, AddNotificationResponseSchema, GetLimitNotificationsRequestSchema, GetNotificationResponseSchema, GetNotificationsResponseSchema, GetUnreadNotificationsRequestSchema



router = APIRouter(
    tags=['notification']
    
)

@router.post(
    '/add/notification',
    response_model=AddNotificationResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description='Add adress',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def add_user_adress_handler(
    scheme: AddNotificationRequestSchema, 
    container=Depends(init_container)
):
    '''Add adress'''
    mediator: Mediator = container.resolve(Mediator)
    
    try:
        notification, *_ = await mediator.handle_command(
            AddNotificationCommand(
                user_id=scheme.user_id,
                text=scheme.text
        ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    return AddNotificationResponseSchema.from_entity(notification=notification)

@router.get(
    '/get',
    response_model=GetNotificationsResponseSchema,
    status_code=status.HTTP_200_OK,
    description='Get limit count of notifications',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_limit_notifications_handler(
    scheme: GetLimitNotificationsRequestSchema,
    container = Depends(init_container)
):
    '''Get limit count of notifications'''
    mediator: Mediator = container.resolve(Mediator)
    try:
        notifications, *_ = await mediator.handle_query(
            GetLimitNotificationsQuery(
                token=scheme.token,
                count_limit=scheme.count_limit
        ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    
    data = []
    for notification in notifications:
        schema = GetNotificationResponseSchema(
            notification_id=notification.oid,
            user_id = notification.user_id,
            notification_text=notification.text,
            is_readed = notification.is_readed,
            time_created = notification.time_created,
        )
        data.append(schema)
    
    return GetNotificationsResponseSchema(data=data)

@router.get(
    '/get/unread',
    response_model=GetNotificationsResponseSchema,
    status_code=status.HTTP_200_OK,
    description='Get unread notifications',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_unread_notifications_handler(
    scheme: GetUnreadNotificationsRequestSchema,
    container = Depends(init_container)
):
    '''Get limit count of notifications'''
    mediator: Mediator = container.resolve(Mediator)
    try:
        notifications, *_ = await mediator.handle_query(
            GetUnreadNotificationsQuery(
                token=scheme.token
        ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    
    data = []
    for notification in notifications:
        schema = GetNotificationResponseSchema(
            notification_id=notification.oid,
            user_id = notification.user_id,
            notification_text = notification.text,
            is_readed = notification.is_readed,
            time_created = notification.time_created,
        )
        data.append(schema)
    
    
    return GetNotificationsResponseSchema(data=data)