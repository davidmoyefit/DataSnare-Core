# NinjaOne RMM Integration

DataSnare-Core will connect to NinjaOne as a partner service. NinjaOne remains an external system; its API access is not a DataSnare project license.

## Reference

- [NinjaOne Public API 2.0](https://oc.ninjarmm.com/apidocs/?links.active=authorization)
- OpenAPI document: `https://app.ninjarmm.com/apidocs/NinjaRMM-API-v2.json`

## OAuth2 authentication

NinjaOne documents OAuth2 authorization-code and implicit grants. Core will use the authorization-code grant because the client secret and token exchange can remain on the server. Core will not use the implicit grant for the integrated application because it would place tokens in a browser context.

Authorization endpoints:

- Authorize: `https://oc.ninjarmm.com/ws/oauth/authorize`
- Token: `https://oc.ninjarmm.com/ws/oauth/token`

The callback must validate the `state` value, exchange the one-time code server-side, encrypt the resulting refresh token, and associate the connection with the authenticated DataSnare tenant. Access tokens should be short-lived and held only in backend memory or an approved secret/token store.

## Planned phases

### Phase 1: Read-only inventory and health

- Store a tenant-scoped NinjaOne connection record.
- Keep credentials and refresh tokens server-side in the Core/AIOps backend.
- Sync organizations, locations, devices, device roles, and groups.
- Import alerts, activities, device health, operating systems, software, disks, volumes, network interfaces, and patch reports.
- Map external organization/device IDs to DataSnare tenant/system IDs.
- Show connection health, last sync time, and API errors in Core.

### Phase 2: Investigation links

- Link DataSnare findings to the originating NinjaOne organization and device.
- Open the corresponding NinjaOne dashboard URL from an evidence record.
- Correlate NinjaOne alerts and activities with AILogScope, AIPerf, AIProcMon, AINetScope, and AIRootCause evidence.
- Add inbound webhooks for alert/activity changes where tenant configuration permits.

### Phase 3: Controlled actions

Management actions must pass DataSnare authorization, project licensing, tenant policy, approval, and audit checks before reaching NinjaOne. Candidate actions include:

- device maintenance scheduling
- reboot
- Windows service control
- script or built-in action execution
- OS/software patch scan and apply
- ticket creation, comments, and updates

No management action should be exposed directly from a browser with stored NinjaOne credentials.

## Connector boundary

The connector should normalize external data into stable DataSnare contracts:

```text
NinjaOne API -> Core/AIOps connector -> normalized systems, alerts, activities, evidence, actions
```

Recommended backend boundaries:

- `ninjaone_connections`: tenant-scoped endpoint and encrypted credential reference
- `ninjaone_sync_jobs`: queued syncs, cursors, retry state, and last successful run
- `ninjaone_external_links`: external organization/device/alert/ticket IDs
- `ninjaone_webhook_events`: verified inbound events and replay status
- `ninjaone_action_audit`: requested action, DataSnare decision, external response, and actor

The browser should receive normalized DataSnare objects, never raw secrets or unfiltered partner responses.

## First implementation slice

The initial connector lives in `backend/app/services/ninjaone.py`. It is deliberately read-only and provides:

- versioned endpoint construction
- bearer-token requests through a server-side `aiohttp` session
- OAuth2 authorization-code URL construction and server-side code exchange
- collection envelope normalization
- stable external entity links for cross-tool evidence

The connector does not persist credentials, expose browser routes, or perform NinjaOne management actions yet. Those belong behind Core/AIOps tenant authentication, encrypted secret storage, licensing checks, and audit/approval gates.

## Core API boundary

The initial Core API is in `backend/app/routes/ninjaone.py`:

- `GET /api/tenants/{tenant_id}/integrations/ninjaone/connection` returns redacted connection metadata.
- `POST /api/tenants/{tenant_id}/integrations/ninjaone/authorize` stores non-secret connection metadata and returns an OAuth2 authorization-code URL.

Both routes require the current temporary `X-Actor` boundary. This is a development seam for route tests, not the final authentication system. The next backend step is replacing the in-memory repository with encrypted, database-backed storage and binding the actor to Core/AIOps identity and tenant permissions.