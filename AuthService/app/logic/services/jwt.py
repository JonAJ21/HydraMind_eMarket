from datetime import datetime, timedelta, timezone
import jwt

from dataclasses import dataclass

from settings.config import settings

        
@dataclass(frozen=True)
class TokenInfo:
    access_token: str
    refresh_token: str | None = None
    token_type: str = 'Bearer'

@dataclass(eq=False)
class JWT:
    @staticmethod
    def encode(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None
    ):
        
        to_encode = payload.copy()        
        now = datetime.now(timezone.utc)
        
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)
        
        to_encode.update({
            'exp': expire,
            'iat': now
        })
        
        
        return jwt.encode(
            payload=to_encode,
            key=private_key,
            algorithm=algorithm
        )  
    
    @staticmethod 
    def decode(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm
    ):
        return jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=[algorithm]
        )
        
    
    
    
    