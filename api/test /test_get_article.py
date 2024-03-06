import pytest
from httpx import AsyncClient
from starlette.status import HTTP_200_OK
from ..database import get_db


@pytest.mark.asyncio
async def test_get_articles(client: AsyncClient, article_api):

    response = await client.get(article_api + "/articles")
    
    assert response.status_code == HTTP_200_OK
    
    assert "articles" in response.json()

    assert "articlesCount" in response.json()
    
    assert isinstance(response.json()["articles"], list)
    
    assert isinstance(response.json()["articlesCount"], int)

