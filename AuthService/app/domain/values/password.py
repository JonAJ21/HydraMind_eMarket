import bcrypt

from dataclasses import dataclass

from domain.values.base import BaseValueObject

@dataclass(frozen=True)
class Password(BaseValueObject):
    value: bytes
    
    @classmethod
    def hashed_password(cls, password: str) -> 'Password':
        salt: bytes = bcrypt.gensalt()

        pwd_bytes: bytes = password.encode()
        return Password(bcrypt.hashpw(pwd_bytes, salt))
    
    
    def __eq__(self, __value: bytes) -> bool:
        try: 
            return bcrypt.checkpw(
                password=__value,
                hashed_password=self.value
            )
        except ValueError:
            return self.value == __value
    
    def validate(self):
        ...
    
    def as_generic_type(self):
        return self.value.decode(encoding='utf-8')