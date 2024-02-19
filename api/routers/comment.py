from couchbase.exceptions import DocumentExistsException
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from ..core.article import query_articles_by_slug
from ..core.user import query_users_by_id
from ..database import get_db
from ..models.article import CommentModel
from ..models.user import UserModel
from ..routers.article import ARTICLE_COLLECTION
from ..schemas.comment import (
    CreateCommentSchema,
    CommentSchema,
    SingleCommentResponseSchema,
    MultipleCommentsResponseSchema
)
from ..schemas.user import ProfileResponseSchema
from ..utils.security import (
    get_current_user_instance
)


router = APIRouter()


COMMENT_COLLECTION = "comment"


@router.post(
    "/articles/{slug}/comments",
    response_model=SingleCommentResponseSchema
)
async def add_article_comment(
    slug: str,
    comment: CreateCommentSchema = Body(..., embed=True),
    user_instance: UserModel = Depends(get_current_user_instance),
    db=Depends(get_db)
):
    article = await query_articles_by_slug(slug, db)
    comment_instance = CommentModel(
        authorId=user_instance.id, **comment.model_dump()
    )
    article.comments = article.comments + (comment_instance,)
    try:
        db.upsert_document(ARTICLE_COLLECTION, article.slug, jsonable_encoder(article))
    except DocumentExistsException:
        raise HTTPException(status_code=409, detail="Article already exists")
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    response_profile = ProfileResponseSchema(**user_instance.model_dump())
    response_comment = CommentSchema(author=response_profile, **comment_instance.model_dump())
    return SingleCommentResponseSchema(comment=response_comment)


@router.get(
    "/articles/{slug}/comments",
    response_model=MultipleCommentsResponseSchema
)
async def get_article_comments(
    slug: str,
    db=Depends(get_db)
):
    article = await query_articles_by_slug(slug, db)
    comments = [CommentModel(**comment)for comment in article.comments]
    comment_authorIds = [comment.authorId for comment in comments]
    comment_authors=[]
    for author_id in comment_authorIds:
        comment_authors.append(await query_users_by_id(author_id, db))
    data = list(zip(range(len(comments)), range(len(comment_authors))))
    return MultipleCommentsResponseSchema.from_comments_and_authors(data)



