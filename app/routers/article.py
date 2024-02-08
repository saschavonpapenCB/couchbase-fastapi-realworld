from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/article",
    tags=["article"],
    responses={404: {"description": "Not found"}},
)


fake_article_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/")
async def read_article():
    return fake_article_db


@router.get("/{article_id}")
async def read_article(article_id: str):
    if article_id not in fake_article_db:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"name": fake_article_db[article_id]["name"], "article_id": article_id}


@router.put(
    "/{article_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_article(article_id: str):
    if article_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the article: plumbus"
        )
    return {"article_id": article_id, "name": "The great Plumbus"}