from datetime import datetime
from typing import List, Tuple
from uuid import uuid4

from pydantic import Field

from models.article import CommentModel
from models.user import UserModel
from schemas.user import Profile

from .base import BaseSchema


def generate_uuid():
    return str(uuid4())


class Comment(BaseSchema):
    id: str = Field(default_factory=generate_uuid, alias="_id")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    body: str
    author: Profile


class SingleCommentResponse(BaseSchema):
    comment: Comment


class MultipleCommentsResponse(BaseSchema):
    comments: List[Comment]

    @classmethod
    def from_comments_and_authors(cls, data: List[Tuple[CommentModel, UserModel]]):
        return cls(
            comments=[{**comment.model_dump(), "author": author} for comment, author in data]
        )


class NewComment(BaseSchema):
    body: str


class ProfileResponse(BaseSchema):
    profile: Profile
