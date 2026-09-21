from __future__ import annotations

import secrets

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel, Field

from app.repositories.partner_connections import PartnerConnectionRecord
from app.services.ninjaone import NinjaOneOAuthConfig


router = APIRouter(prefix="/api/tenants/{tenant_id}/integrations/ninjaone", tags=["NinjaOne"])


class AuthorizationRequest(BaseModel):
    base_url: str = Field(min_length=1)
    client_id: str = Field(min_length=1)
    redirect_uri: str = Field(min_length=1)
    scopes: list[str] = Field(default_factory=list)


def _require_actor(actor: str | None) -> str:
    if not actor or not actor.strip():
        raise HTTPException(status_code=401, detail="DataSnare actor authentication is required")
    return actor.strip()


@router.get("/connection")
async def get_connection(tenant_id: int, request: Request, x_actor: str | None = Header(default=None)):
    _require_actor(x_actor)
    record = await request.app.state.partner_connections.get(tenant_id, "ninjaone")
    if not record:
        return {"provider": "ninjaone", "tenant_id": tenant_id, "connected": False}
    return {
        "provider": record.provider,
        "tenant_id": record.tenant_id,
        "base_url": record.base_url,
        "client_id": record.client_id,
        "redirect_uri": record.redirect_uri,
        "scopes": list(record.scopes),
        "connected": record.connected,
        "updated_at": record.updated_at.isoformat() if record.updated_at else None,
    }


@router.post("/authorize")
async def begin_authorization(
    tenant_id: int,
    body: AuthorizationRequest,
    request: Request,
    x_actor: str | None = Header(default=None),
):
    _require_actor(x_actor)
    state = secrets.token_urlsafe(32)
    record = PartnerConnectionRecord(
        tenant_id=tenant_id,
        provider="ninjaone",
        base_url=body.base_url,
        client_id=body.client_id,
        redirect_uri=body.redirect_uri,
        scopes=tuple(body.scopes),
    )
    await request.app.state.partner_connections.save(record)
    config = NinjaOneOAuthConfig(
        client_id=body.client_id,
        client_secret="server-managed",
        redirect_uri=body.redirect_uri,
    )
    return {
        "provider": "ninjaone",
        "tenant_id": tenant_id,
        "authorization_url": config.authorization_request_url(state, scope=" ".join(body.scopes) or None),
        "state": state,
        "next_step": "redirect_user_to_authorization_url",
    }