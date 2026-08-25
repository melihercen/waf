import httpx
from config import BACKEND_URL

client=httpx.AsyncClient(
    trust_env=False,
    timeout=10.0
)
async def forward_request(
    method,
    path,
    headers,
    body
):
    
    backend_url=BACKEND_URL+path

    response=await client.request(
        method=method, 
        url=backend_url,             
        headers=headers,
        content=body
        )

    return response