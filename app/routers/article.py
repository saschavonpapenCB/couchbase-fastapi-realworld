from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query

from ..models.article import ArticleModel
from ..database import get_db


router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    responses={404: {"description": "Not found"}},
)


EXAMPLE_AUTHOR = "J. K. Rowling"
EXAMPLE_FAVORITE = "Favorited"
EXAMPLE_TAG = "Review"


@router.get(
    "/",
    response_model=list[ArticleModel],
    description="Get a list of article. Optionally, you can filter by tag, author & favorited user. The list can also be limited and offset. \n\n Method: `list_articles`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def list_articles(
    author: Annotated[
        str | None,
        Query(
            description="Author",
            examples=[EXAMPLE_AUTHOR],
            openapi_examples={
                "All": {"value": ""},
                "J. K. Rowling": {"value": "J. K. Rowling"},
                "George Orwell": {"value": "George Orwell"},
            },
        )
    ] = None,
    favorited: Annotated[
        str | None,
        Query(
            description="Favorited",
            examples=[EXAMPLE_FAVORITE],
            openapi_examples={
                "All": {"value": ""},
                "Favorited": {"value": "Favorited"},
                "Not favorited": {"value": "Not favorited"},
            },
        )
    ] = None,
    tag: Annotated[
        str | None,
        Query(
            description="Tag",
            examples=[EXAMPLE_TAG],
            openapi_examples={
                "All": {"value": ""},
                "Review": {"value": "Review"},
                "Trendy": {"value": "Trendy"},
            },
        )
    ] = None,
    limit: Annotated[
        int,
        Query(description="Number of articles to return (page size)"),
    ] = 20,
    offset: Annotated[
        int,
        Query(description="Number of articles to to skip (for pagination)"),
    ] = 0,
    # Need to implement user instance,
    db=get_db,
) -> list[ArticleModel]:
    #TBC
    return {"GET list of articles" : "Returns multiple Articles"}


@router.get(
    "/feed",
    response_model=list[ArticleModel],
    description="Get a list of feed article. Ordered by most recent first. The list can also be limited and offset. \n\n Method: `list_feed_articles`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def list_feed_articles() -> list[ArticleModel]:
    #TBC
    return {"GET list of feed articles" : "Returns multiple Articles"}


@router.get(
    "/{slug}",
    response_model=ArticleModel,
    description="Get a single article. \n\n Method: `get_article`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def get_article(
    slug: str,
    # Need to add user instance,
    db=Depends(get_db),
) -> ArticleModel:
    #TBC
    return {"GET article" : "Returns Article"}


@router.post(
    "/",
    response_model=ArticleModel,
    description="Create a single article. \n\n Method: `create_article`",
    status_code=status.HTTP_201_CREATED,
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def create_article() -> ArticleModel:
    #TBC
    return {"POST create article" : "Returns Article"}


@router.put(
    "/{slug}",
    response_model=ArticleModel,
    description="Update a single article. \n\n Method: `update_article`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def update_article() -> ArticleModel:
    #TBC
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
async def delete_article() -> None:
    #TBC
    return {"DELETE article" : "Does not return"}


@router.post(
    "/{slug}/favorite",
    response_model=ArticleModel,
    description="Favorite a single article. \n\n Method: `favorite_article`",
    status_code=status.HTTP_201_CREATED,
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def favorite_article() -> ArticleModel:
    #TBC
    return {"POST favorite article" : "Returns Article"}


@router.delete(
    "/{slug}/favorite",
    status_code=status.HTTP_200_OK,
    response_model=ArticleModel,
    description="Unfavorite a single article. \n\n Method: `unfavorite_article`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def unfavorite_article() -> ArticleModel:
    #TBC
    return {"DELETE unfavorite article" : "Returns Article"}
