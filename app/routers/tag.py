from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/tags",
    tags=["tags"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def list_tags():
    #TBC
    return {"Get list of tags" : "Returns list of Tags"}