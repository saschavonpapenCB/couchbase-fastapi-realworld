from pydantic import BaseModel, Field
from typing import Tuple

from .identifier import generate_id


class UserModel(BaseModel):
    identifier: str = Field(default_factory=generate_id)
    username: str
    email: str
    hashed_password: str
    bio: str | None = None
    image: str | None = None 
    following_ids: Tuple[str, ...] = ()   
