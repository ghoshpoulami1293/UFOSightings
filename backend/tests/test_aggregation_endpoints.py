import pytest
from bson import ObjectId

def test_get_countries(client, monkeypatch):
    """Test the /countries endpoint returns a list of unique country values."""
    # Mock the aggregate function to return test data
    def fake_aggregate(pipeline):
        # Check if we're grouping by country
        if pipeline and "$group" in pipeline[0] and pipeline[0]["$group"]["_id"] == "$country":
            return [{"_id": "US"}, {"_id": "CA"}, {"_id": "GB"}]
        return []
    
    monkeypatch.setattr("db.ufoSightings.aggregate", fake_aggregate)
    
    # Test the endpoint
    response = client.get("/countries")
    assert response.status_code == 200
    data = response.get_json()
    
    # Check that the response is a list containing the expected countries
    assert isinstance(data, list)
    assert "US" in data
    assert "CA" in data
    assert "GB" in data
    assert len(data) == 3

def test_get_states(client, monkeypatch):
    """Test the /states endpoint returns a list of unique state values."""
    def fake_aggregate(pipeline):
        # Check if we're grouping by state
        if pipeline and "$group" in pipeline[0] and pipeline[0]["$group"]["_id"] == "$state":
            return [{"_id": "CA"}, {"_id": "NY"}, {"_id": "TX"}]
        return []
    
    monkeypatch.setattr("db.ufoSightings.aggregate", fake_aggregate)
    
    # Test the endpoint
    response = client.get("/states")
    assert response.status_code == 200
    data = response.get_json()
    
    # Check that the response is a list containing the expected states
    assert isinstance(data, list)
    assert "CA" in data
    assert "NY" in data
    assert "TX" in data
    assert len(data) == 3

def test_get_shapes(client, monkeypatch):
    """Test the /shapes endpoint returns a list of unique shape values."""
    def fake_aggregate(pipeline):
        # Check if we're grouping by shape
        if pipeline and "$group" in pipeline[0] and pipeline[0]["$group"]["_id"] == "$shape":
            return [{"_id": "circle"}, {"_id": "triangle"}, {"_id": "oval"}]
        return []
    
    monkeypatch.setattr("db.ufoSightings.aggregate", fake_aggregate)
    
    # Test the endpoint
    response = client.get("/shapes")
    assert response.status_code == 200
    data = response.get_json()
    
    # Check that the response is a list containing the expected shapes
    assert isinstance(data, list)
    assert "circle" in data
    assert "triangle" in data
    assert "oval" in data
    assert len(data) == 3

def test_countries_empty_results(client, monkeypatch):
    """Test the /countries endpoint when no results are returned."""
    def fake_aggregate(pipeline):
        return []
    
    monkeypatch.setattr("db.ufoSightings.aggregate", fake_aggregate)
    
    response = client.get("/countries")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data

def test_states_empty_results(client, monkeypatch):
    """Test the /states endpoint when no results are returned."""
    def fake_aggregate(pipeline):
        return []
    
    monkeypatch.setattr("db.ufoSightings.aggregate", fake_aggregate)
    
    response = client.get("/states")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data

def test_shapes_empty_results(client, monkeypatch):
    """Test the /shapes endpoint when no results are returned."""
    def fake_aggregate(pipeline):
        return []
    
    monkeypatch.setattr("db.ufoSightings.aggregate", fake_aggregate)
    
    response = client.get("/shapes")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data