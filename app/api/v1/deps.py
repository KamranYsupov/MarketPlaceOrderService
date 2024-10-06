import aiohttp

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings
from app.core.container import Container
from app.utils.http import get_response_data_or_raise_http_exception


http_bearer = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    access_token = credentials.credentials
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'{settings.auth_users_service_api_v1_url}/users/me/',
            headers={'Authorization': f'Bearer {access_token}'}
        ) as response:
            user_data = await get_response_data_or_raise_http_exception(response)
            user_data['access_token'] = access_token
            
            return user_data

