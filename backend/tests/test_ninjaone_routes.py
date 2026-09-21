import pathlib
import sys

from fastapi.testclient import TestClient


BACKEND_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.main import create_app


def test_connection_requires_actor():
    client = TestClient(create_app())

    response = client.get("/api/tenants/7/integrations/ninjaone/connection")

    assert response.status_code == 401


def test_authorize_stores_redacted_tenant_connection_and_returns_oauth_url():
    client = TestClient(create_app())

    response = client.post(
        "/api/tenants/7/integrations/ninjaone/authorize",
        headers={"X-Actor": "operator@example.com"},
        json={
            "base_url": "https://api.ninjarmm.com",
            "client_id": "ninja-client",
            "redirect_uri": "https://app.datasnare.com/api/integrations/ninjaone/callback",
            "scopes": ["monitoring", "management"],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert "response_type=code" in payload["authorization_url"]
    assert "client_secret" not in payload["authorization_url"]
    assert payload["state"]

    status = client.get(
        "/api/tenants/7/integrations/ninjaone/connection",
        headers={"X-Actor": "operator@example.com"},
    )
    assert status.status_code == 200
    assert status.json()["client_id"] == "ninja-client"
    assert "server-managed" not in status.text