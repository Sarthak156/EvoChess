import sys;sys.path.append('backend')
from fastapi.testclient import TestClient
from app.main import app
c=TestClient(app)
def test_health():assert c.get('/health').json()['status']=='ok'
def test_rules():assert len(c.get('/api/rules').json())==20
