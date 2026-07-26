from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.session import Base,engine
from app.api.routes import router
configure_logging();Base.metadata.create_all(engine)
app=FastAPI(title=settings.app_name,version='1.0.0',description='Adaptive rules chess API')
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origins,allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
app.include_router(router)
@app.get('/')
def root():return {'app':settings.app_name,'version':'1.0.0','status':'ok'}
@app.get('/health')
def health():return {'status':'ok'}