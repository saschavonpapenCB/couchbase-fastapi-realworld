from fastapi.testclient import TestClient

from ..main import api

client = TestClient(api)


class TestArticle:
    def test_read_article(
        self, couchbase_client, article_api, article_collection, helpers
    ):
        """Test the reading of an article"""
        article_data = {
            "slug": "example-article-slug548e72a3",
            "title": "Example Article Title",
            "description": "Example article description.",
            "body": "Example article body.",
            "tagList": ["ExampleTag1", "ExampleTag2"],
            "createdAt": "2024-03-06T09:05:14.377741",
            "updatedAt": "2024-03-06T09:05:14.377748",
            "author": {
                "id": "example-article-id",
                "username": "exampleuser",
                "email": "exampleuser@example.com",
                "hashed_password": "68b77a946d17400f0cca8ddd86b145015e5d01cb89c8d953bb4067adebb91fbe",
                "bio": None,
                "image": None,
                "following_ids": [],
            },
            "favoritedUserIds": [],
            "comments": [],
        }
        helpers.delete_existing_document(
            couchbase_client, article_collection, article_data["slug"]
        )
        couchbase_client.insert_document(
            article_collection, key=article_data["slug"], doc=article_data
        )
        response = client.get(url=f"{article_api}/{article_data['slug']}")
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["article"]["slug"] == article_data["slug"]
        assert response_data["article"]["title"] == article_data["title"]
        assert response_data["article"]["description"] == article_data["description"]
        assert response_data["article"]["body"] == article_data["body"]

        couchbase_client.delete_document(article_collection, key=article_data["slug"])
