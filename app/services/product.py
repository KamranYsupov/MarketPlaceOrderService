import aiohttp

from uuid import UUID
from typing import List, Sequence, Union

from fastapi import Depends
from app.core.config import settings
from app.utils.http import get_response_data_or_raise_http_exception
  


class ProductHttpService:
    async def get_products_by_ids(
        self,
        ids: List[Union[str, UUID]],
        fields: Sequence[str] = (
            'id',
            'name',
            'price',
            'quantity',
            'rating',
            'description',
        ),
    ) -> dict[str]:
        ids_string = ', '.join(f'"{id_}"' for id_ in ids)
        query_field_name = 'getProductsByIds'
        products_query = f""" 
        query ProductQuery {{ 
            {query_field_name}(ids: [{ids_string}]) {{ 
            {" ".join(fields)} 
            }} 
        }} 
        """

        async with aiohttp.ClientSession() as client_session:
            async with client_session.post(
                f'{settings.product_service_api_v1_url}/graphql',
                json={'query': products_query}
            ) as response:
                
                response_data = await get_response_data_or_raise_http_exception(response)
                products_data = response_data['data'][query_field_name]
                
                return products_data
            
    async def bulk_update(
        self,
        update_data: List[dict],
        access_token: str
    ) -> dict[str]:
        async with aiohttp.ClientSession() as client_session:
            async with client_session.put(
                f'{settings.product_service_api_v1_url}/products/update',
                json=update_data,
                headers={'Authorization': f'Bearer {access_token}'}
            ) as response:
                
                return await get_response_data_or_raise_http_exception(response)