from pydantic import SecretStr

from .base import BaseSchema


class AuthenticationSchema(BaseSchema):
    email: str
    password: SecretStr


class RegistrationSchema(BaseSchema):
    username: str
    email: str
    password: str


class UserResponseSchema(BaseSchema):
    email: str
    token: str
    username: str
    bio: str | None = None
    image: str | None = None


class UserWrapperSchema(BaseSchema):
    user: UserResponseSchema


class UpdateUserSchema(BaseSchema):
    email: str | None = None
    token: str | None = None
    username: str | None = None
    bio: str | None = None
    image: str | None = None


class ProfileResponseSchema(BaseSchema):
    username: str
    bio: str | None
    image: str | None
    following: bool = False


class ProfileWrapperSchema(BaseSchema):
    profile: ProfileResponseSchema
