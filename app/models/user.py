from typing import Tuple

from pydantic import BaseModel, Field
from uuid import uuid4


def generate_uuid():
    return str(uuid4())


class UserModel(BaseModel):
    id: str = Field(default_factory=generate_uuid, alias="_id")
    username: str
    email: str
    hashed_password: str
    bio: str | None = None
    image: str | None = None
    following_ids: Tuple[str, ...] = ()


class ProfileModel(BaseModel):
    username: str
    bio: str | None = None
    image: str | None = None
    following: bool = False