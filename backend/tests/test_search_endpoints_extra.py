import pytest

def test_search_country_valid(client):
    # Assume searching for "US" returns data
    response = client.get("/sightings/country/US?page=1")
    assert response.status_code == 200
    data = response.get_json()
    assert "data" in data
    assert "total" in data
    assert "page" in data
    assert "limit" in data
    # Total should be greater than 0 if data is returned
    assert data["total"] > 0

def test_search_country_no_results(client):
    # For a non-existing country code, the total should be 0 and data list empty
    response = client.get("/sightings/country/ZZ?page=1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 0
    assert data["data"] == []

def test_search_city_valid(client):
    # Assume searching for city "TestCity" returns data
    response = client.get("/sightings/city/TestCity?page=1")
    assert response.status_code == 200
    data = response.get_json()
    assert "data" in data
    assert "total" in data
    assert "page" in data
    assert "limit" in data
    assert data["total"] > 0

def test_search_city_no_results(client):
    # For a city that does not exist, there should be no results
    response = client.get("/sightings/city/Nowhere?page=1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 0
    assert data["data"] == []

def test_search_shape_valid(client):
    # Assume searching for shape "circle" returns records with shape "circle"
    response = client.get("/sightings/shape/circle?page=1")
    assert response.status_code == 200
    data = response.get_json()
    assert "data" in data
    assert "total" in data
    assert "page" in data
    assert "limit" in data
    # Check that each result's shape field contains "circle" (case-insensitive)
    for doc in data["data"]:
        assert "circle".lower() in doc.get("shape", "").lower()

def test_search_shape_no_results(client):
    # For an unknown shape, no results should be returned
    response = client.get("/sightings/shape/unknown?page=1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 0
    assert data["data"] == []

def test_search_comments_valid(client):
    # Assume searching for comment "TestComment" returns records with that comment
    response = client.get("/sightings/comments/TestComment?page=1")
    assert response.status_code == 200
    data = response.get_json()
    assert "data" in data
    assert "total" in data
    assert "page" in data
    assert "limit" in data
    # Verify that each result's comments field includes the keyword (case-insensitive)
    for doc in data["data"]:
        assert "testcomment" in doc.get("comments", "").lower()

def test_search_comments_no_results(client):
    # For a comment that does not match any record, total should be 0 and data empty
    response = client.get("/sightings/comments/nomatch?page=1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 0
    assert data["data"] == []

def test_search_state_valid(client):
    # Assume searching for state "TS" returns data
    response = client.get("/sightings/state/TS?page=1")
    assert response.status_code == 200
    data = response.get_json()
    assert "data" in data
    assert "total" in data
    assert "page" in data
    assert "limit" in data
    assert data["total"] > 0

def test_search_state_no_results(client):
    # For a state code that does not match any record, total should be 0 and data list empty
    response = client.get("/sightings/state/XX?page=1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 0
    assert data["data"] == []