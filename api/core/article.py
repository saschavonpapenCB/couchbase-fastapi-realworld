from fastapi import HTTPException

from ..models.article import ArticleModel


async def query_articles_by_slug(
    slug: str,
    db
) -> ArticleModel:
    query = """
            SELECT article.slug,
                article.title,
                article.description,
                article.body,
                article.tagList,
                article.createdAt,
                article.updatedAt,
                article.favorited,
                article.favoritesCount,
                article.author
            FROM article as article
            WHERE article.slug=$slug
            ORDER BY article.createdAt;
        """
    try:
        queryResult = db.query(query, slug=slug)
        article_data = [r for r in queryResult][0]
        return ArticleModel(**article_data)
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")