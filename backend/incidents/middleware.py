from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query = parse_qs(scope["query_string"].decode())
        token = query.get("token")

        if token:
            scope["user"] = await self.get_user(token[0])
        else:
            scope["user"] = None  # IMPORTANT: no AnonymousUser import

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token):
        from rest_framework_simplejwt.authentication import JWTAuthentication

        jwt_auth = JWTAuthentication()
        validated = jwt_auth.get_validated_token(token)
        return jwt_auth.get_user(validated)
