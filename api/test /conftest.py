import pytest
from couchbase.exceptions import DocumentNotFoundException
from ..database import get_db  

BASE = "http://127.0.0.1:8000"
BASE_URI = f"{BASE}/api/v1"

@pytest.fixture(scope="session")
def couchbase_client():
    couchbase_client = get_db()
    return couchbase_client

@pytest.fixture(scope="module")
def article_api():
    return f"{BASE_URI}/article"

@pytest.fixture(scope="module")
def article_collection():
    return "article"

class Helpers:
    @staticmethod
    def delete_existing_document(couchbase_client, collection, key):
        try:
            couchbase_client.delete_document(collection, key)
        except DocumentNotFoundException:
            pass

@pytest.fixture(autouse=True, scope="session")
def helpers():
    return Helpers

