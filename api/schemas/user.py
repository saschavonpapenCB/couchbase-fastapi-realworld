from pydantic import SecretStr

from .base import BaseSchema


class AuthenticationSchema(BaseSchema):
    email: str
    password: SecretStr


class RegistrationSchema(BaseSchema):
    username: str
    email: str
    password: str


class UserSchema(BaseSchema):
    email: str
    token: str
    username: str
    bio: str | None = None
    image: str | None = None


class UserResponseSchema(BaseSchema):
    user: UserSchema


class UpdateUserSchema(BaseSchema):
    email: str | None = None
    token: str | None = None
    username: str | None = None
    bio: str | None = None
    image: str | None = None


class ProfileSchema(BaseSchema):
    username: str
    bio: str | None
    image: str | None
    following: bool = False


class ProfileResponseSchema(BaseSchema):
    profile: ProfileSchema
