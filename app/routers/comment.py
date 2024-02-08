from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(
    prefix="/articles",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)


@router.post("/{slug}/comments")
async def add_article_comment():
    #TBC
    return {"POST add article comment" : "Returns Comment"}


@router.get("/{slug}/comments")
async def list_article_comments():
    #TBC
    return {"GET list article comments" : "Returns multiple Comments"}


@router.delete("/{slug}/comments/{id}")
async def delete_comment():
    #TBC
    return {"DELETE article comment" : "Does not return anything"}