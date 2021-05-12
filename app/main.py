from fastapi import FastAPI
from app.api.api import api_router
from app.settings.config import settings

from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title='P2PEnergy', openapi_url='/api/p2p/openapi.json'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router, prefix='/api/p2p')