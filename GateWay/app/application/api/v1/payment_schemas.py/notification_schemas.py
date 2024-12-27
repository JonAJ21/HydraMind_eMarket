
from pydantic import BaseModel


class AddNotificationRequestScheme(BaseModel):
    user_id: str
    text: str