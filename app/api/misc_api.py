from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from prometheus_client import CollectorRegistry, generate_latest
from app.schemas.misc_schemas import HealthcheckSchema
from app.clients.prometheus.client import REQUEST_COUNT
from app.config import settings

misc_router = APIRouter()


@misc_router.get("/healthcheck", response_model=HealthcheckSchema)
def healthcheck(request: Request):
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    return HealthcheckSchema(status="OK", version=settings.app.app_version)


@misc_router.get("/metrics", response_class=PlainTextResponse)
def metrics(request: Request):
    registry = CollectorRegistry()
    return  generate_latest(registry)
