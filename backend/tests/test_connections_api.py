from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_validate_normalizes():
    r = client.post("/connections/validate", json={"discom": "SBPDCL", "ca_number": " 1234-56789 "})
    assert r.status_code == 200
    assert r.json() == {"discom": "SBPDCL", "ca_number_normalized": "123456789"}


def test_validate_rejects_bad_ca():
    r = client.post("/connections/validate", json={"discom": "NBPDCL", "ca_number": "12"})
    assert r.status_code == 422


def test_validate_rejects_unknown_discom():
    r = client.post("/connections/validate", json={"discom": "OTHER", "ca_number": "123456789"})
    assert r.status_code == 422
