from fastapi import APIRouter, Depends, status, Body

from ..models.article import ArticleModel
from ..models.user import UserModel
from ..database import get_db
from ..schemas.article import (
    MultipleArticlesResponse,
    NewArticle,
    SingleArticleResponse,
    UpdateArticle,
)
from ..utils.security import get_current_user, get_current_user_optional


router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    responses={404: {"description": "Not found"}},
)


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
    author: str | None = None,
    favorited: str | None = None,
    tag: str | None = None,
    limit: int = 20,
    offset: int = 0,
    user_instance: UserModel | None = Depends(get_current_user_optional),
):
    # Need to implement response return
    return {"GET list of articles" : "Returns multiple Articles"}


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
):
    # Need to implement response return
    return {"GET article" : "Returns Article"}


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
    new_article: NewArticle = Body(..., embed=True, alias="article"),
    user_instance: UserModel = Depends(get_current_user),
):
    # Need to implement response return
    return {"POST create article" : "Returns Article"}


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
):
    # Need to implement response return
    return {"PUT update article" : "Returns Article"}


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
