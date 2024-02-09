from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/tags",
    tags=["tags"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/",
    response_model=list[str],
    description="Get a list of tags. \n\n Method: `list_tags`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def list_tags() -> list[str]:
    #TBC
    return {"Get list of tags" : "Returns list of Tags"}