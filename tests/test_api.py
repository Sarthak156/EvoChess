import sys;sys.path.append('backend')
import asyncio
import httpx
from app.main import app
async def request(path:str):
 transport=httpx.ASGITransport(app=app)
 async with httpx.AsyncClient(transport=transport,base_url='http://test') as client:return await client.get(path)
def test_health():assert asyncio.run(request('/health')).json()['status']=='ok'
def test_rules():assert len(asyncio.run(request('/api/rules')).json())==20
