import aiohttp
from aiohttp.client_reqrep import ClientResponse
from fastapi import HTTPException
from starlette import status


async def get_response_data_or_raise_http_exception(
    response: ClientResponse,
    excpected_status_code: int = status.HTTP_200_OK,
):
    response_data = await response.json()
    if response.status == excpected_status_code:
        return response_data
            
    response_detail = response_data.get('detail')
    exc_data = {}

    if response_detail:
        exc_data['status_code'] = response.status
        exc_data['detail'] = response_detail 
    else:
        exc_data['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
        
    raise HTTPException(**exc_data)
