from couchbase.exceptions import DocumentExistsException
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from ..database import get_db
from ..models.article import ArticleModel
from ..models.user import UserModel
from ..schemas.article import (
    ArticleWrapperSchema,
    CreateArticleRequestSchema
)
from ..utils.security import (
    get_current_user_instance,
    get_current_user_optional_instance
)


router = APIRouter()


ARTICLE_COLLECTION = "article"


@router.post(
    "/articles",
    response_model=ArticleWrapperSchema
)
async def create_article(
    article: CreateArticleRequestSchema = Body(..., embed=True),
    user_instance: UserModel = Depends(get_current_user_instance),
    db=Depends(get_db)
):
    response_article = ArticleModel(author=user_instance, **article.model_dump())
    response_article.tagList.sort()

    try:
        db.insert_document(ARTICLE_COLLECTION, response_article.slug, jsonable_encoder(response_article))
    except DocumentExistsException:
        raise HTTPException(status_code=409, detail="Article already exists")
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    
    return ArticleWrapperSchema.from_article_instance(response_article, user_instance)


@router.get(
    "/articles/{slug}",
    response_model=ArticleWrapperSchema
)
async def get_single_article(
    slug: str,
    user_instance: UserModel | None = Depends(get_current_user_optional_instance),
    db=Depends(get_db)
):
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
            ORDER BY airline.createdAt;
        """
    try:
        queryResult = db.query(query, slug=slug)
        article_data = [r for r in queryResult][0]
        article = ArticleModel(**article_data)
        return ArticleWrapperSchema.from_article_instance(article, user_instance)
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
