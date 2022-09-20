from datetime import datetime, timedelta

from itsdangerous.url_safe import URLSafeTimedSerializer

from api.config import settings
from api.responses import exceptions


class TokenService:
    def __init__(self):
        self.serializer = URLSafeTimedSerializer(
            secret_key=settings.SECRET_KEY
        )

    def create_token(self,
                     expires_minutes: int,  # Время жизни токена
                     **params):
        if expires_minutes:
            params['expires'] = (datetime.utcnow() + timedelta(minutes=expires_minutes)).strftime('%m/%d/%Y, %H:%M:%S')
        token = self.serializer.dumps(params)
        return token

    def decode_token(self,
                     token: str):
        try:
            data = self.serializer.loads(token)
        except:
            raise exceptions.EXCEPTION_TOKEN
        if datetime.strptime(data['expires'], '%m/%d/%Y, %H:%M:%S') < datetime.utcnow():
            raise exceptions.EXCEPTION_TOKEN
        return data
