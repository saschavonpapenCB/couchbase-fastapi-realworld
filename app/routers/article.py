from fastapi import APIRouter, Depends, status, Body
from couchbase.exceptions import DocumentExistsException, CouchbaseException
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from ..core.exceptions import ArticleNotFoundException, NotArticleAuthorException
from datetime import datetime

from ..models.article import ArticleModel
from ..models.user import UserModel
from ..database import get_db
from ..schemas.article import (
    MultipleArticlesResponse,
    NewArticle,
    SingleArticleResponse,
    UpdateArticle,
)
from ..utils.security import (
    get_current_user,
    get_current_user_optional,
    get_user_instance
)


router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    responses={404: {"description": "Not found"}},
)


ARTICLE_COLLECTION = "article"


@router.get(
    "/",
    response_model=MultipleArticlesResponse,
    description="Get a list of article. Optionally, you can filter by tag, author & favorited user. The list can also be limited and offset. \n\n Method: `list_articles`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def list_articles(
    author: str | None = None, # Consider adding query example metadata
    favorited: str | None = None,
    tag: str | None = None,
    limit: int = 20,
    offset: int = 0,
    user_instance: UserModel | None = Depends(get_current_user_optional),
    db = Depends(get_db),
):
    if author: # Haven't tested ORDER BY with datetimes
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
            WHERE article.author=$author 
            ORDER BY article.createdAt
            LIMIT $limit 
            OFFSET $offset;
        """
    elif favorited:
        instance = await get_user_instance(db, username=favorited)
        # Need to implement search for favorited user
        pass
    elif tag:
        # Implement way to search tagList for tag.
        pass
    else:
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
            ORDER BY airline.createdAt
            LIMIT $limit
            OFFSET $offset;
        """
    try:
        queryResult = db.query(query, author=author, favorited=favorited, tag=tag, limit=limit, offset=offset)
        article_list = [r for r in queryResult]
        print(article_list)
    except Exception as e:
        return f"Unexpected error: {e}", 500
    if article_list is None:
        return MultipleArticlesResponse(articles=[], articles_count=0)
    response = MultipleArticlesResponse(articles=article_list, articlesCount=len(article_list))
    return response


@router.get(
    "/feed",
    response_model=MultipleArticlesResponse,
    description="Get a list of feed article. Ordered by most recent first. The list can also be limited and offset. \n\n Method: `list_feed_articles`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def list_feed_articles(
    limit: int = 20,
    offset: int = 0,
    user_instance: UserModel = Depends(get_current_user),
):
    # Need to implement response return
    return {"GET list of feed articles" : "Returns multiple Articles"}


@router.get(
    "/{slug}",
    response_model=SingleArticleResponse,
    description="Get a single article. \n\n Method: `get_article`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def get_article(
    slug: str,
    user_instance: UserModel | None = Depends(get_current_user_optional),
    db = Depends(get_db),
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
        return SingleArticleResponse.from_article_instance(article, user_instance)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@router.post(
    "/",
    response_model=SingleArticleResponse,
    description="Create a single article. \n\n Method: `create_article`",
    status_code=status.HTTP_201_CREATED,
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def create_article(
    article: NewArticle = Body(..., embed=True, alias="article"),
    user: UserModel = Depends(get_current_user),
    db = Depends(get_db),
):
    user_instance = await get_user_instance(db, username=user.username)
    new_article = ArticleModel(author=user_instance, **article.model_dump())
    new_article.tag_list.sort()
    try:
        db.insert_document(ARTICLE_COLLECTION, new_article.slug, jsonable_encoder(new_article))
    except DocumentExistsException:
        raise HTTPException(status_code=409, detail="Article already exists")
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except CouchbaseException as ce:
        raise HTTPException(status_code=500, detail=f"CouchbaseException: {ce}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    return SingleArticleResponse.from_article_instance(new_article, user_instance)


@router.put(
    "/{slug}",
    response_model=SingleArticleResponse,
    description="Update a single article. \n\n Method: `update_article`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def update_article(
    slug: str,
    update_data: UpdateArticle = Body(..., embed=True, alias="article"),
    current_user: UserModel = Depends(get_current_user),
    db=Depends(get_db),
):
    article = await get_article(slug=slug)
    if current_user != article.author:
        raise NotArticleAuthorException()

    patch_dict = update_data.dict(exclude_none=True)
    for name, value in patch_dict.items():
        setattr(article, name, value)
    article.updated_at = datetime.utcnow()
    try:
        db.upsert_document(ARTICLE_COLLECTION,article.slug,jsonable_encoder(article))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    return SingleArticleResponse.from_article_instance(article, current_user)


@router.delete(
    "/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a single article. \n\n Method: `delete_article`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def delete_article(
    slug: str,
    current_user: UserModel = Depends(get_current_user),
):
    # Need to implement response return
    return {"DELETE article" : "Does not return"}


@router.post(
    "/{slug}/favorite",
    response_model=SingleArticleResponse,
    description="Favorite a single article. \n\n Method: `favorite_article`",
    status_code=status.HTTP_201_CREATED,
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def favorite_article(
    slug: str,
    current_user: UserModel = Depends(get_current_user),
):
    # Need to implement response return
    return {"POST favorite article" : "Returns Article"}


@router.delete(
    "/{slug}/favorite",
    status_code=status.HTTP_200_OK,
    response_model=SingleArticleResponse,
    description="Unfavorite a single article. \n\n Method: `unfavorite_article`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def unfavorite_article(
    slug: str,
    current_user: UserModel = Depends(get_current_user),
):
    # Need to implement response return
    return {"DELETE unfavorite article" : "Returns Article"}
