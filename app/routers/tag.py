from fastapi import APIRouter, Depends, HTTPException

from ..schemas.tag import TagsResponse


router = APIRouter(
    prefix="/tags",
    tags=["tags"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/",
    response_model=TagsResponse,
    description="Get a list of tags. \n\n Method: `list_tags`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def list_tags():
    # Need to implement response return
    return {"Get list of tags" : "Returns list of Tags"}