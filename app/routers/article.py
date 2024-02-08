from fastapi import APIRouter, Depends, HTTPException, status
from ..models.article import ArticleModel

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    responses={404: {"description": "Not found"}},
)


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
async def list_articles():
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
async def list_feed_articles():
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
async def get_article():
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
async def create_article():
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
async def update_article():
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
async def delete_article():
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
async def favorite_article():
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
async def unfavorite_article():
    #TBC
    return {"DELETE unfavorite article" : "Returns Article"}
