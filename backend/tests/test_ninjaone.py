import pytest

from app.services.ninjaone import (
    NinjaOneConnection,
    normalize_collection,
    normalize_external_entity,
)


def test_connection_builds_versioned_endpoint_without_duplicate_slashes():
    connection = NinjaOneConnection(
        base_url="https://api.ninjarmm.com/",
        access_token="server-only-token",
    )

    assert connection.endpoint("/devices") == "https://api.ninjarmm.com/v2/devices"


@pytest.mark.parametrize(
    "payload, expected",
    [
        ([{"id": 1}], [{"id": 1}]),
        ({"data": [{"id": 2}]}, [{"id": 2}]),
        ({"items": [{"id": 3}]}, [{"id": 3}]),
        ({"unexpected": True}, []),
    ],
)
def test_normalize_collection_handles_common_api_envelopes(payload, expected):
    assert normalize_collection(payload) == expected


def test_normalize_external_entity_creates_cross_tool_link_shape():
    result = normalize_external_entity(
        {"id": 42, "hostname": "server-01", "organizationId": 9},
        entity_type="device",
    )

    assert result == {
        "provider": "ninjaone",
        "entity_type": "device",
        "external_id": "42",
        "name": "server-01",
    }