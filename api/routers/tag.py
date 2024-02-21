from fastapi import APIRouter, Depends, HTTPException

from ..database import get_db
from ..schemas.tag import TagsResponseSchema


router = APIRouter(
    tags=["tags"],
    responses={404: {"description": "Not found"}},
)


@router.get("/tags", response_model=TagsResponseSchema)
async def get_tags(db=Depends(get_db)
):
    query = """
            SELECT article.tagList
            FROM article as article;
        """
    try:
        queryResult = db.query(query)
        result_list = [r for r in queryResult]
        if len(result_list) > 0:
            all_tags = [tags for tagList in result_list for tags in tagList["tagList"]]
        else:
            all_tags = []
        return TagsResponseSchema(tags=all_tags)
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
