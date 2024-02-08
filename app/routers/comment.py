from fastapi import APIRouter, Depends, HTTPException, status
from ..models.article import CommentModel


router = APIRouter(
    prefix="/articles",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/{slug}/comments",
    response_model=CommentModel,
    description="Create a single article comment. \n\n Method: `add_article_comment`",
    status_code=status.HTTP_201_CREATED,
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)


async def add_article_comment():
    #TBC
    return {"POST add article comment" : "Returns Comment"}


@router.get(
        "/{slug}/comments",
    response_model=list[CommentModel],
    description="List multiple article comments. \n\n Method: `list_article_comments`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def list_article_comments():
    #TBC
    return {"GET list article comments" : "Returns multiple Comments"}


@router.delete(
        "/{slug}/comments/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a single article comment. \n\n Method: `delete_comment`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def delete_comment():
    #TBC
    return {"DELETE article comment" : "Does not return anything"}