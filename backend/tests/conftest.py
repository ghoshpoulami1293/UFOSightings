
import sys
import os
import importlib.util


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app", "db.py"))
spec = importlib.util.spec_from_file_location("db", db_path)
db = importlib.util.module_from_spec(spec)
spec.loader.exec_module(db)
sys.modules["db"] = db  


import io
import pytest
from bson import ObjectId
from backend.app import app, ufoSightings, fs
from backend.app import routes
routes.init_routes(app)

app.config['TESTING'] = True


class FakeCursor:
    def __init__(self, records):
        self.records = records

    def sort(self, sort_params):
        # For testing purposes, perform a basic sort on each field.
        # sort_params is a list of tuples [(field, order)], where order==1 means ascending, -1 descending.
        for field, order in reversed(sort_params):
            self.records.sort(key=lambda x: x.get(field, None), reverse=(order == -1))
        return self

    def skip(self, offset):
        # Simulate skipping the first offset records.
        self.records = self.records[offset:]
        return self

    def limit(self, n):
        # Limit the results to n records.
        self.records = self.records[:n]
        return self

    def __iter__(self):
        return iter(self.records)


@pytest.fixture(autouse=True)
def setup_mocks(monkeypatch):
    def fake_find(query, projection):
        # If the query contains "$or" (e.g. for search_word), simulate returning 15 records.
        if "$or" in query:
            docs = []
            for i in range(15):
                docs.append({
                    "_id": ObjectId(),
                    "city": f"TestCity{i}",
                    "comments": "TestComment",
                    "country": "US",
                    "shape": "circle",
                    "state": "TS",
                    "location": {"coordinates": [-80.0, 40.0]}
                })
            return FakeCursor(docs)
        # For specific field queries:
        elif "country" in query:
            regex_val = query["country"].get("$regex", "").upper()
            if regex_val == "US":
                doc = {
                    "_id": ObjectId(),
                    "city": "TestCity",
                    "comments": "TestComment",
                    "country": "US",
                    "shape": "circle",
                    "state": "TS",
                    "location": {"coordinates": [-80.0, 40.0]}
                }
                return FakeCursor([doc])
            else:
                return FakeCursor([])
        elif "state" in query:
            regex_val = query["state"].get("$regex", "").upper()
            if regex_val == "TS":
                doc = {
                    "_id": ObjectId(),
                    "city": "TestCity",
                    "comments": "TestComment",
                    "country": "US",
                    "shape": "circle",
                    "state": "TS",
                    "location": {"coordinates": [-80.0, 40.0]}
                }
                return FakeCursor([doc])
            else:
                return FakeCursor([])
        elif "city" in query:
            regex_val = query["city"].get("$regex", "").lower()
            if regex_val == "testcity":
                doc = {
                    "_id": ObjectId(),
                    "city": "TestCity",
                    "comments": "TestComment",
                    "country": "US",
                    "shape": "circle",
                    "state": "TS",
                    "location": {"coordinates": [-80.0, 40.0]}
                }
                return FakeCursor([doc])
            else:
                return FakeCursor([])
        elif "shape" in query:
            regex_val = query["shape"].get("$regex", "").lower()
            if regex_val == "circle":
                doc = {
                    "_id": ObjectId(),
                    "city": "TestCity",
                    "comments": "TestComment",
                    "country": "US",
                    "shape": "circle",
                    "state": "TS",
                    "location": {"coordinates": [-80.0, 40.0]}
                }
                return FakeCursor([doc])
            else:
                return FakeCursor([])
        elif "comments" in query:
            regex_val = query["comments"].get("$regex", "").lower()
            if "testcomment" in regex_val:
                doc = {
                    "_id": ObjectId(),
                    "city": "TestCity",
                    "comments": "TestComment",
                    "country": "US",
                    "shape": "circle",
                    "state": "TS",
                    "location": {"coordinates": [-80.0, 40.0]}
                }
                return FakeCursor([doc])
            else:
                return FakeCursor([])
        # For /search_nearby: if query includes "location" (or "$geoWithin") return one record.
        elif ("location" in query) or ("$geoWithin" in query):
            doc = {
                "_id": ObjectId(),
                "city": "TestCity",
                "comments": "TestComment",
                "country": "US",
                "shape": "circle",
                "state": "TS",
                "location": {"coordinates": [-80.0, 40.0]}
            }
            return FakeCursor([doc])
        else:
            return FakeCursor([])

    monkeypatch.setattr(ufoSightings, "find", fake_find)

    def fake_find_one(query):
        _id = query.get("_id")
        if str(_id) == "000000000000000000000000":
            return None
        return {
            "_id": _id,
            "datetime": "2025-03-07 12:00",
            "city": "TestCity",
            "state": "TS",
            "shape": "circle",
            "image": ObjectId()
        }
    monkeypatch.setattr(ufoSightings, "find_one", fake_find_one)
    monkeypatch.setattr(ufoSightings, "update_one", lambda query, update: None)

    # Adjust count_documents to be consistent with fake_find results:
    def fake_count_documents(query):
        # For "$or" queries, simulate 15 documents;
        # Otherwise, count the number of records that fake_find would return.
        if "$or" in query:
            return 15
        else:
            # Create a temporary FakeCursor based on the query.
            cursor = fake_find(query, {})
            return len(cursor.records)
    monkeypatch.setattr(ufoSightings, "count_documents", fake_count_documents)

    def fake_fs_get(oid):
        dummy_content = b"dummy_image_content"
        return io.BytesIO(dummy_content)
    monkeypatch.setattr(fs, "get", fake_fs_get)


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
