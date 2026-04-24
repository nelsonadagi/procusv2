from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from urllib.parse import parse_qs

@database_sync_to_async
def get_user(token_key):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:
    """
    Custom token auth middleware for Django Channels 2/3
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope['query_string'].decode())
        token_key = query_string.get('token')
        if token_key:
            print(f"WS Token Found: {token_key[0]}")
            scope['user'] = await get_user(token_key[0])
            print(f"WS User: {scope['user']}")
        else:
            print("No WS Token found")
            scope['user'] = AnonymousUser()
        return await self.inner(scope, receive, send)
