from pydantic import BaseModel, Field, root_validator
from datetime import datetime
from typing import List, Tuple
from uuid import uuid4

from app.models.user import UserModel
from .ObjectId import ObjectId


def generate_random_str():
    s = str(uuid4())
    return s.split("-")[0]


def generate_uuid():
    return str(uuid4())


class CommentModel(BaseModel):
    """Comment embedded model with a unique id field"""

    id: ObjectId = Field(default_factory=ObjectId)
    body: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    authorId: ObjectId


class ArticleModel(BaseModel):
    slug: str
    # NOTE: slug is not a primary field because it could change and this would imply to
    # change all the references
    title: str
    description: str
    body: str
    tag_list: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    author: UserModel
    favorited_user_ids: Tuple[ObjectId, ...] = ()
    comments: Tuple[CommentModel, ...] = ()

    @root_validator(pre=True)
    def generate_slug(cls, values):
        if values.get("slug") is not None:
            return values
        title = values.get("title", "")
        words = title.split()[:5]
        words = [w.lower() for w in words]
        slug = "-".join(words) + f"-{generate_random_str()}"
        values["slug"] = slug
        # Note on why the tag_list is sorted:
        # https://github.com/gothinkster/realworld/issues/839
        if values.get("tag_list") is not None and isinstance(values["tag_list"], list):
            values["tag_list"].sort()
        return values
