export const PARTNER_CONNECTION_STATES = {
  planned: 'planned',
  connected: 'connected',
  degraded: 'degraded',
  disconnected: 'disconnected',
};

export const PARTNER_CAPABILITIES = {
  inventoryRead: 'inventory.read',
  healthRead: 'health.read',
  alertsRead: 'alerts.read',
  activitiesRead: 'activities.read',
  ticketRead: 'ticket.read',
  ticketWrite: 'ticket.write',
  deviceActions: 'device.actions',
};

export const ninjaOnePartner = {
  id: 'ninjaone',
  name: 'NinjaOne RMM',
  provider: 'NinjaOne',
  documentationUrl: 'https://app.ninjarmm.com/apidocs/',
  apiVersion: 'v2',
  connectionState: PARTNER_CONNECTION_STATES.planned,
  credentialBoundary: 'backend',
  requiresSeparateLicense: false,
  capabilities: [
    PARTNER_CAPABILITIES.inventoryRead,
    PARTNER_CAPABILITIES.healthRead,
    PARTNER_CAPABILITIES.alertsRead,
    PARTNER_CAPABILITIES.activitiesRead,
    PARTNER_CAPABILITIES.ticketRead,
  ],
};

export function hasPartnerCapability(partner, capability) {
  return partner.capabilities.includes(capability);
}