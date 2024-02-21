from typing import Tuple

from couchbase.exceptions import DocumentExistsException
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from ..core.article import query_articles_by_slug
from ..core.exceptions import NotCommentAuthorException, CommentNotFoundException
from ..core.user import query_users_db
from ..database import get_db
from ..models.article import CommentModel
from ..models.user import UserModel
from ..routers.article import ARTICLE_COLLECTION
from ..schemas.comment import (
    CommentResponseSchema,
    CreateCommentSchema,
    MultipleCommentsResponseSchema,
    SingleCommentResponseSchema,
)
from ..schemas.user import ProfileResponseSchema
from ..utils.security import get_current_user_instance


router = APIRouter(
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)
COMMENT_COLLECTION = "comment"


@router.post("/articles/{slug}/comments", response_model=SingleCommentResponseSchema)
async def add_article_comment(
    slug: str,
    comment: CreateCommentSchema = Body(..., embed=True),
    user_instance: UserModel = Depends(get_current_user_instance),
    db=Depends(get_db),
):
    article = await query_articles_by_slug(slug, db)
    comment_instance = CommentModel(authorId=user_instance.id, **comment.model_dump())
    article.comments = article.comments + (comment_instance,)
    try:
        db.upsert_document(ARTICLE_COLLECTION, article.slug, jsonable_encoder(article))
        response_profile = ProfileResponseSchema(**user_instance.model_dump())
        response_comment = CommentResponseSchema(
            author=response_profile, **comment_instance.model_dump()
        )
        return SingleCommentResponseSchema(comment=response_comment)
    except DocumentExistsException:
        raise HTTPException(status_code=409, detail="Article already exists")
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@router.get("/articles/{slug}/comments", response_model=MultipleCommentsResponseSchema)
async def get_article_comments(slug: str, db=Depends(get_db)):
    article = await query_articles_by_slug(slug, db)
    comments = [comment for comment in article.comments]
    comment_authorIds = [comment.authorId for comment in comments]
    comment_authors = []
    for author_id in comment_authorIds:
        comment_authors.append(await query_users_db(db, id=author_id))
    data = []
    for index, comment in enumerate(comments):
        data.append((comment, comment_authors[index]))
    return MultipleCommentsResponseSchema.from_comments_and_authors(data)


@router.delete("/articles/{slug}/comments/{id}")
async def delete_article_comment(
    slug: str,
    id: str,
    user_instance: UserModel = Depends(get_current_user_instance),
    db=Depends(get_db),
):
    article = await query_articles_by_slug(slug, db)
    comments = [comment for comment in article.comments]
    if not comments:
        raise CommentNotFoundException()
    for index, comment in enumerate(comments):
        if comment.id == id:
            if comment.authorId == user_instance.id:
                article.comments = (
                    article.comments[:index] + article.comments[index + 1 :]
                )
    try:
        db.upsert_document(ARTICLE_COLLECTION, article.slug, jsonable_encoder(article))
    except DocumentExistsException:
        raise HTTPException(status_code=409, detail="Article already exists")
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
