from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from ..core.article import query_articles_by_slug
from ..core.exceptions import CommentNotFoundException
from ..core.user import query_users_db
from ..database import get_db
from ..models.article import CommentModel
from ..models.user import UserModel
from ..routers.article import ARTICLE_COLLECTION
from ..schemas.comment import (
    CommentSchema,
    CreateCommentSchema,
    MultipleCommentsResponseSchema,
    SingleCommentResponseSchema,
)
from ..schemas.user import ProfileSchema
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
    """Queries db for article instance by slug, creates comment instance from create schema, adds comment instance \
        to article instance, upserts article instance and returns comment schema."""
    article = await query_articles_by_slug(slug, db)
    comment_instance = CommentModel(authorId=user_instance.id, **comment.model_dump())
    article.comments = article.comments + (comment_instance,)
    try:
        db.upsert_document(ARTICLE_COLLECTION, article.slug, jsonable_encoder(article))
        return SingleCommentResponseSchema(comment=CommentSchema(
            author=ProfileSchema(**user_instance.model_dump()),
            **comment_instance.model_dump(),
        ))
    except TimeoutError:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")


@router.get("/articles/{slug}/comments", response_model=MultipleCommentsResponseSchema)
async def get_article_comments(slug: str, db=Depends(get_db)):
    """Queries db for article instance by slug, queries db for user instances by id of article comments, creates \
        comment schemas and returns multiple comments schema."""
    article = await query_articles_by_slug(slug, db)
    comments = [comment for comment in article.comments]
    data = [
        (comment, await query_users_db(db, id=comment.authorId)) for comment in comments
    ]
    return MultipleCommentsResponseSchema.from_comments_and_authors(data)


@router.delete("/articles/{slug}/comments/{id}")
async def delete_article_comment(
    slug: str,
    id: str,
    user_instance: UserModel = Depends(get_current_user_instance),
    db=Depends(get_db),
):
    """Queries db for article instance by slug, identifies comment by comment ID and user ID, removes comment from \
        article instance and upserts article instance to db."""
    try:
        article = await query_articles_by_slug(slug, db)
        comment = next(
            (
                c
                for c in article.comments
                if c.id == id and c.authorId == user_instance.id
            ),
            None,
        )
        if comment:
            article.comments = tuple(c for c in article.comments if c.id != id)
            db.upsert_document(
                ARTICLE_COLLECTION, article.slug, jsonable_encoder(article)
            )
        else:
            raise CommentNotFoundException()
    except TimeoutError:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")
