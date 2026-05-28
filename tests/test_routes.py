import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
import notes_service
from app import app


@pytest.fixture(autouse=True)
def reset():
    notes_service.reset()


@pytest.fixture
def client():
    app.testing = True
    return app.test_client()


def test_get_all_notes(client):
    resp = client.get("/notes")
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_create_note_defaults_starred_false(client):
    resp = client.post("/notes", json={"title": "T", "content": "C"})
    assert resp.status_code == 201
    assert resp.get_json()["starred"] is False


def test_create_note_missing_fields_returns_400(client):
    resp = client.post("/notes", json={"title": "T"})
    assert resp.status_code == 400


def test_patch_star_toggles(client):
    client.post("/notes", json={"title": "T", "content": "C"})
    resp = client.patch("/notes/1/star")
    assert resp.status_code == 200
    assert resp.get_json()["starred"] is True


def test_patch_star_twice_toggles_back(client):
    client.post("/notes", json={"title": "T", "content": "C"})
    client.patch("/notes/1/star")
    resp = client.patch("/notes/1/star")
    assert resp.get_json()["starred"] is False


def test_patch_star_unknown_id_returns_404(client):
    resp = client.patch("/notes/999/star")
    assert resp.status_code == 404


def test_get_notes_filter_starred(client):
    client.post("/notes", json={"title": "A", "content": "1"})
    client.post("/notes", json={"title": "B", "content": "2"})
    client.patch("/notes/1/star")
    resp = client.get("/notes?filter=starred")
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["id"] == 1


def test_get_notes_filter_starred_empty(client):
    client.post("/notes", json={"title": "A", "content": "1"})
    resp = client.get("/notes?filter=starred")
    assert resp.status_code == 200
    assert resp.get_json() == []
