from fastapi import APIRouter, Depends, Body, status

from ..models.user import UserModel
from ..schemas.comment import MultipleCommentsResponse, NewComment, SingleCommentResponse
from ..schemas.user import User
from ..utils.security import get_current_user


router = APIRouter(
    prefix="/articles",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/{slug}/comments",
    response_model=SingleCommentResponse,
    description="Create a single article comment. \n\n Method: `add_article_comment`",
    status_code=status.HTTP_201_CREATED,
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def add_article_comment(
    slug: str,
    new_comment: NewComment = Body(..., embed=True, alias="comment"),
    user_instance: UserModel = Depends(get_current_user),
):
    # Need to implement response return
    return {"POST add article comment" : "Returns Comment"}


@router.get(
    "/{slug}/comments",
    response_model=MultipleCommentsResponse,
    description="List multiple article comments. \n\n Method: `list_article_comments`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def list_article_comments(
    slug: str,
):
    # Need to implement response return
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
async def delete_comment(
    slug: str,
    id: str, # Might need replacing
    user_instance: User = Depends(get_current_user),
):
    # Need to implement response return
    return {"DELETE article comment" : "Does not return anything"}