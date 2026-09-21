"""Read-only NinjaOne Public API connector and normalization helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

import aiohttp


class NinjaOneError(RuntimeError):
    """Raised when a NinjaOne request cannot be completed safely."""


@dataclass(frozen=True)
class NinjaOneConnection:
    """Tenant-scoped connection settings; secrets stay outside this object."""

    base_url: str
    access_token: str
    api_version: str = "v2"

    def endpoint(self, resource: str) -> str:
        base = self.base_url.rstrip("/")
        version = self.api_version.strip("/")
        path = resource.strip("/")
        return f"{base}/{version}/{path}"


class NinjaOneClient:
    """Small read-only client for the first Core sync phase."""

    def __init__(self, connection: NinjaOneConnection, session: aiohttp.ClientSession):
        self.connection = connection
        self.session = session

    async def get(self, resource: str, *, params: Mapping[str, Any] | None = None) -> Any:
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.connection.access_token}",
        }
        try:
            async with self.session.get(
                self.connection.endpoint(resource),
                headers=headers,
                params=params,
            ) as response:
                if response.status >= 400:
                    detail = (await response.text())[:500]
                    raise NinjaOneError(f"NinjaOne {response.status}: {detail}")
                return await response.json()
        except aiohttp.ClientError as exc:
            raise NinjaOneError("NinjaOne request failed") from exc

    async def organizations(self) -> list[dict[str, Any]]:
        return normalize_collection(await self.get("organizations"))

    async def devices(self) -> list[dict[str, Any]]:
        return normalize_collection(await self.get("devices"))

    async def alerts(self) -> list[dict[str, Any]]:
        return normalize_collection(await self.get("alerts"))

    async def activities(self) -> list[dict[str, Any]]:
        return normalize_collection(await self.get("activities"))


def normalize_collection(payload: Any) -> list[dict[str, Any]]:
    """Convert common NinjaOne list envelopes into stable object lists."""

    if isinstance(payload, list):
        values = payload
    elif isinstance(payload, Mapping):
        values = payload.get("data", payload.get("items", payload.get("results", [])))
    else:
        values = []
    return [dict(item) for item in values if isinstance(item, Mapping)]


def normalize_external_entity(entity: Mapping[str, Any], *, entity_type: str) -> dict[str, Any]:
    """Return a stable DataSnare link shape without leaking raw credentials."""

    external_id = entity.get("id", entity.get("uid"))
    name = entity.get("name", entity.get("displayName", entity.get("hostname")))
    return {
        "provider": "ninjaone",
        "entity_type": entity_type,
        "external_id": str(external_id) if external_id is not None else None,
        "name": str(name) if name is not None else None,
    }