from fastapi import APIRouter
from app.api.api_v1.endpoints import memecoins, analysis, social, alerts

api_router = APIRouter()

api_router.include_router(memecoins.router, prefix="/memecoins", tags=["memecoins"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(social.router, prefix="/social", tags=["social"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"]) 