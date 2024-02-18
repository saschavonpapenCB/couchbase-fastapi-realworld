from couchbase.exceptions import DocumentExistsException
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from ..database import get_db
from ..models.article import ArticleModel
from ..models.user import UserModel
from ..schemas.article import (
    ArticleWrapperSchema,
    CreateArticleRequestSchema,
    MultipleArticlesWrapperSchema
)
from ..utils.security import (
    get_current_user_instance,
    get_current_user_optional_instance,
    query_db_for_user
)


router = APIRouter()


ARTICLE_COLLECTION = "article"


@router.get("/articles", response_model=MultipleArticlesWrapperSchema)
async def get_articles(
    author: str | None = None,
    favorited: str | None = None,
    tag: str | None = None,
    limit: int = 20,
    offset: int = 0,
    user_instance: UserModel | None = Depends(get_current_user_optional_instance),
    db=Depends(get_db)
):
    
    if author:
        favorited_identifier = None
        query = """
            SELECT article.slug,
                article.title,
                article.description,
                article.body,
                article.tagList,
                article.createdAt,
                article.updatedAt,
                article.author,
                article.favoritedUserIds,
                article.comments
            FROM article as article 
            WHERE article.author.username=$author
            ORDER BY article.createdAt
            LIMIT $limit
            OFFSET $offset;
        """
    elif favorited:
        favorited_user = await query_db_for_user(db, username=favorited)
        favorited_identifier = favorited_user.identifier
        query = """
            SELECT article.slug,
                article.title,
                article.description,
                article.body,
                article.tagList,
                article.createdAt,
                article.updatedAt,
                article.author,
                article.favoritedUserIds,
                article.comments
            FROM article as article 
            WHERE $favoritedId IN article.favoritedUserIds
            ORDER BY article.createdAt
            LIMIT $limit
            OFFSET $offset;
        """
    elif tag:
        favorited_identifier = None
        query = """
            SELECT article.slug,
                article.title,
                article.description,
                article.body,
                article.tagList,
                article.createdAt,
                article.updatedAt,
                article.author,
                article.favoritedUserIds,
                article.comments
            FROM article as article 
            WHERE $tag IN article.tagList
            ORDER BY article.createdAt
            LIMIT $limit
            OFFSET $offset;
        """
    else:
        favorited_identifier = None
        query = """
            SELECT article.slug,
                article.title,
                article.description,
                article.body,
                article.tagList,
                article.createdAt,
                article.updatedAt,
                article.author,
                article.favoritedUserIds,
                article.comments
            FROM article as article 
            ORDER BY article.createdAt
            LIMIT $limit
            OFFSET $offset;
        """
    if query is None:
        return MultipleArticlesWrapperSchema(articles=[], articles_count=0)
    
    try:
        queryResult = db.query(
            query, author=author, favoritedId=favorited_identifier,
            tag=tag, limit=limit, offset=offset
        )
        article_list = [r for r in queryResult]
        for article in article_list:
            article = ArticleModel(**article)
        response = MultipleArticlesWrapperSchema(articles=article_list, articlesCount=len(article_list))
        return response
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


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
            ORDER BY article.createdAt;
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
