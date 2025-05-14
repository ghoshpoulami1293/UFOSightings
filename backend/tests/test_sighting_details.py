import base64
from bson import ObjectId
from backend.app import ufoSightings

def test_get_sighting_not_found(client, monkeypatch):
    monkeypatch.setattr(ufoSightings, "find_one", lambda query: None)
    response = client.get("/sighting/000000000000000000000000")
    assert response.status_code == 404

def test_get_sighting_with_image(client, monkeypatch):
    test_oid = ObjectId()
    def fake_find_one(query):
        return {
            "_id": test_oid,
            "datetime": "2025-03-07 12:00",
            "city": "TestCity",
            "state": "TS",
            "shape": "circle",
            "image": ObjectId()
        }
    monkeypatch.setattr(ufoSightings, "find_one", fake_find_one)
    response = client.get(f"/sighting/{str(test_oid)}")
    data = response.get_json()
    assert data["_id"] == str(test_oid)
    decoded = base64.b64decode(data["image"])
    assert decoded == b"dummy_image_content"

def test_add_comment_sighting_not_found(client, monkeypatch):
    monkeypatch.setattr(ufoSightings, "find_one", lambda query: None)
    response = client.post("/sighting/000000000000000000000000/comment", json={"comment": "Test"})
    assert response.status_code == 404

def test_add_comment_empty(client, monkeypatch):
    test_oid = ObjectId()
    monkeypatch.setattr(ufoSightings, "find_one", lambda query: {"_id": test_oid})
    response = client.post(f"/sighting/{str(test_oid)}/comment", json={"comment": " "})
    assert response.status_code == 400

def test_add_comment_valid(client, monkeypatch):
    test_oid = ObjectId()
    monkeypatch.setattr(ufoSightings, "find_one", lambda query: {"_id": test_oid, "user_comments": []})
    update_called = {"flag": False}
    def fake_update_one(query, update):
        update_called["flag"] = True
    monkeypatch.setattr(ufoSightings, "update_one", fake_update_one)
    response = client.post(f"/sighting/{str(test_oid)}/comment", json={"comment": "Test comment"})
    data = response.get_json()
    assert response.status_code == 200
    assert data.get("success") is True
    assert update_called["flag"] is True
