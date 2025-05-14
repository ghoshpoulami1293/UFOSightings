import base64
from bson import ObjectId

# Test /search_word endpoints
def test_search_word_no_keyword(client):
    response = client.get("/search_word")
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_search_word_with_keyword(client):
    # Without explicit pagination, the default page=1 should be used
    response = client.get("/search_word?q=test")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    # For "$or" queries, total should be 15
    assert data["total"] == 15

def test_search_word_pagination_page1(client):
    # Request page 1; should return LIMIT records (LIMIT=10)
    response = client.get("/search_word?q=test&page=1")
    assert response.status_code == 200
    data = response.get_json()
    # Check that the response contains pagination fields
    assert "data" in data
    assert "total" in data
    assert "page" in data
    assert "limit" in data
    # For the $or query branch, total should be 15 and page 1 returns 10 records
    assert data["total"] == 15
    assert data["page"] == 1
    assert data["limit"] == 10
    assert len(data["data"]) == 10

def test_search_word_pagination_page2(client):
    # Request page 2; should return the remaining 5 records
    response = client.get("/search_word?q=test&page=2")
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 15
    assert data["page"] == 2
    assert data["limit"] == 10
    # Page 2 should return 15 - 10 = 5 records
    assert len(data["data"]) == 5

# Pagination tests for /search_nearby endpoint
def test_search_nearby_invalid_params(client):
    response = client.get("/search_nearby")
    assert response.status_code == 400

def test_search_nearby_pagination(client):
    # For search_nearby, the fake_find default branch returns 1 record
    response = client.get("/search_nearby?lat=40.0&lon=-80.0&radius=10&page=1")
    assert response.status_code == 200
    data = response.get_json()
    # For this endpoint, total is 1, page is 1, and limit is 10
    assert data["total"] == 1
    assert data["page"] == 1
    assert data["limit"] == 10
    assert len(data["data"]) == 1

# Pagination tests for /sightings/country/<country_code>
def test_search_country_no_results(client):
    response = client.get("/sightings/country/XX")
    data = response.get_json()
    # Expecting an empty data list
    assert isinstance(data, dict)
    assert data["data"] == []

def test_search_country_pagination(client):
    response = client.get("/sightings/country/US?page=1")
    data = response.get_json()
    # The fake finder returns 1 document for matching country queries
    assert data["total"] == 1
    assert data["page"] == 1
    assert data["limit"] == 10
    assert len(data["data"]) == 1
    # Requesting page 2 should yield no records
    response2 = client.get("/sightings/country/US?page=2")
    data2 = response2.get_json()
    assert data2["data"] == []

# Pagination tests for /sightings/city/<city_name>
def test_search_city_no_results(client):
    response = client.get("/sightings/city/NonExistingCity")
    data = response.get_json()
    assert isinstance(data, dict)
    assert data["data"] == []

def test_search_city_pagination_page1(client):
    response = client.get("/sightings/city/TestCity?page=1")
    data = response.get_json()
    # The fake finder returns 1 document for matching city queries
    assert data["total"] == 1
    assert data["page"] == 1
    assert data["limit"] == 10
    assert len(data["data"]) == 1

def test_search_city_pagination_page2(client):
    response = client.get("/sightings/city/TestCity?page=2")
    data = response.get_json()
    # Since total is 1, page 2 should return an empty list
    assert data["data"] == []

# Pagination tests for /sightings/shape/<shape_name>
def test_search_shape_no_results(client):
    response = client.get("/sightings/shape/NonExistingShape")
    data = response.get_json()
    assert isinstance(data, dict)
    assert data["data"] == []

def test_search_shape_pagination_page1(client):
    response = client.get("/sightings/shape/Circle?page=1")
    data = response.get_json()
    # The fake finder returns 1 document for matching shape queries
    assert data["total"] == 1
    assert data["page"] == 1
    assert data["limit"] == 10
    assert len(data["data"]) == 1

def test_search_shape_pagination_page2(client):
    response = client.get("/sightings/shape/Circle?page=2")
    data = response.get_json()
    # Since total is 1, page 2 should return an empty list
    assert data["data"] == []

# Pagination tests for /sightings/comments/<comment>
def test_search_comments_no_results(client):
    response = client.get("/sightings/comments/NoComment")
    data = response.get_json()
    assert isinstance(data, dict)
    assert data["data"] == []

def test_search_comments_pagination_page1(client):
    response = client.get("/sightings/comments/TestComment?page=1")
    data = response.get_json()
    # The fake finder returns 1 document for matching comments queries
    assert data["total"] == 1
    assert data["page"] == 1
    assert data["limit"] == 10
    assert len(data["data"]) == 1

def test_search_comments_pagination_page2(client):
    response = client.get("/sightings/comments/TestComment?page=2")
    data = response.get_json()
    # Since total is 1, page 2 should return an empty list
    assert data["data"] == []

# Pagination tests for /sightings/state/<state_code>
def test_search_state_no_results(client):
    response = client.get("/sightings/state/XX")
    data = response.get_json()
    assert isinstance(data, dict)
    assert data["data"] == []

def test_search_state_pagination_page1(client):
    response = client.get("/sightings/state/TS?page=1")
    data = response.get_json()
    # The fake finder returns 1 document for matching state queries
    assert data["total"] == 1
    assert data["page"] == 1
    assert data["limit"] == 10
    assert len(data["data"]) == 1

def test_search_state_pagination_page2(client):
    response = client.get("/sightings/state/TS?page=2")
    data = response.get_json()
    # Since total is 1, page 2 should return an empty list
    assert data["data"] == []
