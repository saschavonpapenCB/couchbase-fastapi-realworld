from pydantic import Field
from pydantic.types import SecretStr
from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    SECRET_KEY: SecretStr = Field(
        "a91e4985fb8dc2120b9aa9dd5c891b1c9f1127c74edd7080413359bd5fee9b54"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


# Make this a singleton to avoid reloading it from the env everytime
SETTINGS = _Settings()
