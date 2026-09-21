from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Protocol


@dataclass(frozen=True)
class PartnerConnectionRecord:
    tenant_id: int
    provider: str
    base_url: str
    client_id: str
    redirect_uri: str
    scopes: tuple[str, ...]
    connected: bool = False
    updated_at: datetime | None = None


class PartnerConnectionRepository(Protocol):
    async def get(self, tenant_id: int, provider: str) -> PartnerConnectionRecord | None: ...

    async def save(self, record: PartnerConnectionRecord) -> PartnerConnectionRecord: ...


class InMemoryPartnerConnectionRepository:
    """Replaceable repository for local development and route tests."""

    def __init__(self):
        self._records: dict[tuple[int, str], PartnerConnectionRecord] = {}

    async def get(self, tenant_id: int, provider: str) -> PartnerConnectionRecord | None:
        return self._records.get((tenant_id, provider))

    async def save(self, record: PartnerConnectionRecord) -> PartnerConnectionRecord:
        saved = replace(record, updated_at=datetime.now(timezone.utc))
        self._records[(saved.tenant_id, saved.provider)] = saved
        return saved