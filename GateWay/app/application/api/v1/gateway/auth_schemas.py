
from pydantic import BaseModel


class RegisterUserRequestSchema(BaseModel):
    login: str
    password: str
    
    def json(self):
        return {'login': self.login,
                'password': self.password}
