# DataSnare-Core

The shared DataSnare suite shell for `app.datasnare.com`.

Core owns the suite-level navigation and the integration contract for:

- shared identity and session handoff
- per-project license visibility
- project launch URLs
- future organization, billing, and account settings

The individual tools remain independently deployable. Update `src/App.jsx` when a production deployment URL changes, or move the registry to a Core API when the identity and licensing services are available.

## Local development

```powershell
npm install
npm run dev
```

## Production shape

Deploy the built app at `https://app.datasnare.com`. Each registry entry currently points to a stable path on that host so the projects can later be mounted behind the same gateway without changing the Core UI.
