from fastapi import FastAPI

from app.repositories.partner_connections import InMemoryPartnerConnectionRepository
from app.routes.ninjaone import router as ninjaone_router


def create_app(*, partner_connections=None) -> FastAPI:
    app = FastAPI(title="DataSnare-Core API")
    app.state.partner_connections = partner_connections or InMemoryPartnerConnectionRepository()
    app.include_router(ninjaone_router)
    return app


app = create_app()