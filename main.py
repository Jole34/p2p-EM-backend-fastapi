from fastapi import FastAPI
from app.api.api import api_router
from app.settings.config import settings

app = FastAPI(
    title='P2PEnergy', openapi_url='/api/p2p/openapi.json'
)

app.include_router(api_router, prefix='/api/p2p')