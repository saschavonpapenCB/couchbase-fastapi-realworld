from typing import Tuple

from pydantic import BaseModel
from uuid import UUID


class UserModel(BaseModel):
    id: UUID
    username: str
    email: str
    hashed_password: str
    bio: str | None = None
    image: str | None = None
    following_ids: Tuple[id, ...] = ()
