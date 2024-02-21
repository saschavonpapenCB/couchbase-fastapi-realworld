from typing import Tuple

from pydantic import BaseModel, Field

from .identifier import generate_id


class UserModel(BaseModel):
    id: str = Field(default_factory=generate_id)
    username: str
    email: str
    hashed_password: str
    bio: str | None = None
    image: str | None = None
    following_ids: Tuple[str, ...] = ()
