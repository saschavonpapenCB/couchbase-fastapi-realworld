from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def list_articles():
    #TBC
    return {"GET list of articles" : "Returns multiple Articles"}


@router.get("/feed")
async def list_feed_articles():
    #TBC
    return {"GET list of feed articles" : "Returns multiple Articles"}


@router.get("/{slug}")
async def get_article():
    #TBC
    return {"GET article" : "Returns Article"}


@router.post("/")
async def create_article():
    #TBC
    return {"POST create article" : "Returns Article"}


@router.put("/{slug}")
async def update_article():
    #TBC
    return {"PUT update article" : "Returns Article"}


@router.delete("/{slug}")
async def delete_article():
    #TBC
    return {"DELETE article" : "Does not return"}


@router.post("/{slug}/favorite")
async def favorite_article():
    #TBC
    return {"POST favorite article" : "Returns Article"}


@router.post("/{slug}/favorite")
async def unfavorite_article():
    #TBC
    return {"POST unfavorite article" : "Returns Article"}
