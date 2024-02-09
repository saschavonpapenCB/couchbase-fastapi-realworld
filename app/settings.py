from pydantic import Field
from pydantic.types import SecretStr
from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    SECRET_KEY: SecretStr = Field(
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


# Make this a singleton to avoid reloading it from the env everytime
SETTINGS = _Settings()
