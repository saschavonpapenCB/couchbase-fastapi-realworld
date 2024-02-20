from datetime import datetime
from typing import List, Tuple

from ..models.article import CommentModel
from ..models.user import UserModel
from ..schemas.user import ProfileResponseSchema

from .base import BaseSchema


class CommentResponseSchema(BaseSchema):
    id: str
    createdAt: datetime
    updatedAt: datetime
    body: str
    author: ProfileResponseSchema


class SingleCommentResponseSchema(BaseSchema):
    comment: CommentResponseSchema


class MultipleCommentsResponseSchema(BaseSchema):
    comments: List[CommentResponseSchema]

    @classmethod
    def from_comments_and_authors(cls, data: List[Tuple[CommentModel, UserModel]]):
        return cls(
            comments=[{**comment.model_dump(), "author": author} for comment, author in data]
        )


class CreateCommentSchema(BaseSchema):
    body: str
