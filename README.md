# DataSnare-Core

The shared DataSnare suite shell for `app.datasnare.com`.

Core owns the suite-level navigation and the integration contract for:

- shared identity and session handoff
- per-project license visibility
- project launch URLs
- future organization, billing, and account settings

Each tool remains independently deployable and can be licensed on its own. The full app suite adds shared identity, scoped session handoff, cross-tool navigation, and a single view of the user's project entitlements without coupling the tools' release cycles.

Update `src/App.jsx` when a production deployment URL changes, or move the registry to a Core API when the identity and licensing services are available.

## Local development

```powershell
npm install
npm run dev
```

## Production shape

Deploy the built app at `https://app.datasnare.com`. Each registry entry points to a stable project path on that host. A project may also be deployed and sold independently; the suite gateway simply supplies the shared account context when the customer has access to more than one tool.
