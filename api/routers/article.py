from datetime import datetime

from couchbase.exceptions import DocumentExistsException
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from ..core.article import query_articles_by_slug
from ..core.exceptions import NotArticleAuthorException
from ..database import get_db
from ..models.article import ArticleModel
from ..models.user import UserModel
from ..schemas.article import (
    ArticleResponseSchema,
    CreateArticleSchema,
    MultipleArticlesResponseSchema,
    UpdateArticleSchema,
)
from ..utils.security import (
    get_current_user_instance,
    get_current_user_optional_instance,
    get_user_instance,
)


router = APIRouter(
    tags=["articles"],
    responses={404: {"description": "Not found"}},
)
ARTICLE_COLLECTION = "article"


@router.get("/articles", response_model=MultipleArticlesResponseSchema)
async def get_articles(
    author: str | None = None,
    favorited: str | None = None,
    tag: str | None = None,
    limit: int = 20,
    offset: int = 0,
    user_instance: UserModel | None = Depends(get_current_user_optional_instance),
    db=Depends(get_db),
):
    if author:
        favorited_id = None
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
        favorited_user = await get_user_instance(db, username=favorited)
        favorited_id = favorited_user.id
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
        favorited_id = None
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
        favorited_id = None
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
        return MultipleArticlesResponseSchema(articles=[], articles_count=0)
    try:
        queryResult = db.query(
            query,
            author=author,
            favoritedId=favorited_id,
            tag=tag,
            limit=limit,
            offset=offset
        )
        article_list = [ArticleModel(**r) for r in queryResult]
        response = MultipleArticlesResponseSchema.from_article_instances(
            article_list, len(article_list), user_instance
        )
        return response
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@router.get("/articles/feed", response_model=MultipleArticlesResponseSchema)
async def get_feed_articles(
    limit: int = 20,
    offset: int = 0,
    user_instance: UserModel = Depends(get_current_user_instance),
    db=Depends(get_db),
):
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
    try:
        queryResult = db.query(
            query, favoritedId=user_instance.id, limit=limit, offset=offset
        )
        article_list = [r for r in queryResult]
        for article in article_list:
            article = ArticleModel(**article)
        response = MultipleArticlesResponseSchema(
            articles=article_list, articlesCount=len(article_list)
        )
        return response
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@router.post("/articles", response_model=ArticleResponseSchema)
async def create_article(
    article: CreateArticleSchema = Body(..., embed=True),
    user_instance: UserModel = Depends(get_current_user_instance),
    db=Depends(get_db),
):
    response_article = ArticleModel(author=user_instance, **article.model_dump())
    response_article.tagList.sort()
    try:
        db.insert_document(
            ARTICLE_COLLECTION,
            response_article.slug,
            jsonable_encoder(response_article)
        )
        return ArticleResponseSchema.from_article_instance(response_article, user_instance)
    except DocumentExistsException:
        raise HTTPException(status_code=409, detail="Article already exists")
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@router.get("/articles/{slug}", response_model=ArticleResponseSchema)
async def get_single_article(
    slug: str,
    user_instance: UserModel | None = Depends(get_current_user_optional_instance),
    db=Depends(get_db),
):
    article_model = await query_articles_by_slug(slug, db)
    return ArticleResponseSchema.from_article_instance(article_model, user_instance)


@router.put("/articles/{slug}", response_model=ArticleResponseSchema)
async def update_article(
    slug: str,
    article: UpdateArticleSchema = Body(..., embed=True),
    current_user: UserModel = Depends(get_current_user_instance),
    db=Depends(get_db),
):
    article_instance = await query_articles_by_slug(slug, db)
    if current_user != article_instance.author:
        raise NotArticleAuthorException()
    patch_dict = article.model_dump(exclude_none=True)
    for name, value in patch_dict.items():
        setattr(article_instance, name, value)
    article_instance.updatedAt = datetime.utcnow()
    try:
        db.upsert_document(
            ARTICLE_COLLECTION,
            article_instance.slug,
            jsonable_encoder((article_instance))
        )
        return ArticleResponseSchema.from_article_instance(
            article_instance,
            current_user
        )
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@router.post("/articles/{slug}/favorite", response_model=ArticleResponseSchema)
async def favorite_article(
    slug: str,
    current_user: UserModel = Depends(get_current_user_instance),
    db=Depends(get_db),
):
    article = await query_articles_by_slug(slug, db)
    favorited_set = {*article.favoritedUserIds, current_user.id}
    article.favoritedUserIds = tuple(favorited_set)
    try:
        db.upsert_document(ARTICLE_COLLECTION, article.slug, jsonable_encoder(article))
        return ArticleResponseSchema.from_article_instance(article, current_user)
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@router.delete("/articles/{slug}/favorite", response_model=ArticleResponseSchema)
async def unfavorite_article(
    slug: str,
    current_user: UserModel = Depends(get_current_user_instance),
    db=Depends(get_db),
):
    article = await query_articles_by_slug(slug, db)
    favorited_set = {*article.favoritedUserIds} - {current_user.id}
    article.favoritedUserIds = tuple(favorited_set)
    try:
        db.upsert_document(ARTICLE_COLLECTION, article.slug, jsonable_encoder(article))
        return ArticleResponseSchema.from_article_instance(article, current_user)
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@router.delete("/articles/{slug}")
async def delete_article(
    slug: str,
    current_user: UserModel = Depends(get_current_user_instance),
    db=Depends(get_db),
):
    article = await query_articles_by_slug(slug, db)
    if current_user.id != article.author.id:
        raise NotArticleAuthorException()
    try:
        db.delete_document(ARTICLE_COLLECTION, article.slug)
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
