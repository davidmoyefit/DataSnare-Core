# NinjaOne RMM Integration

DataSnare-Core will connect to NinjaOne as a partner service. NinjaOne remains an external system; its API access is not a DataSnare project license.

## Reference

- [NinjaOne Public API 2.0](https://app.ninjarmm.com/apidocs/)
- OpenAPI document: `https://app.ninjarmm.com/apidocs/NinjaRMM-API-v2.json`

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