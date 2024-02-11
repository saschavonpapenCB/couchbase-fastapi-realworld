from datetime import datetime, timedelta
from typing import cast

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, ValidationError
from passlib.context import CryptContext
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from jose import JWTError, jwt

from ..core.exceptions import CredentialsException, NotAuthenticatedException
from ..models.user import UserModel
from ..database import get_db, CouchbaseClient
from ..settings import SETTINGS
from ..schemas.user import User


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenContent(BaseModel):
    username: str


PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


class OAuth2PasswordToken(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str | None = None,
        scopes: dict | None = None,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=False)

    async def __call__(self, request: Request) -> str | None: # Supposed to set the return types default value to None. Unsure.
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "token":
            return None
        return cast(str, param)


OAUTH2_SCHEME = OAuth2PasswordToken(tokenUrl="/users")


app = FastAPI()


def verify_password(plain_password, hashed_password):
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password):
    return PWD_CONTEXT.hash(password)


async def get_user_instance(
    db: CouchbaseClient,
    username: str | None = None,
    email: str | None = None,
):
    """Get a user instance from its username"""
    if username is not None:
        query = """
            SELECT client.email,
                client.token,
                client.username,
                client.bio,
                client.image,
                client.hashed_password
            FROM client as client 
            WHERE client.username=$username;
        """
    elif email is not None:
        query = """
            SELECT client.email,
                client.token,
                client.username,
                client.bio,
                client.image,
                client.hashed_password
            FROM client as client 
            WHERE client.email=$email;
        """
    else:
        return None
    
    try:
        queryResult = db.query(query, username=username, email=email)
        user_data = [r for r in queryResult][0]
        user = UserModel(**user_data)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


async def authenticate_user(
    db: CouchbaseClient,
    email: str,
    password: str
):
    """Verify the User/Password pair against the DB content"""
    user = await get_user_instance(db, email=email)
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(user: UserModel):
    token_content = TokenContent(username=user.username)
    expire = datetime.utcnow() + timedelta(minutes=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": token_content.model_dump_json()}
    encoded_jwt = jwt.encode(
        to_encode, SETTINGS.SECRET_KEY.get_secret_value(), algorithm=SETTINGS.ALGORITHM
    )
    return str(encoded_jwt)


async def get_current_user_instance(
    token: str | None = Depends(OAUTH2_SCHEME),
):
    """Decode the JWT and return the associated User"""
    if token is None:
        raise NotAuthenticatedException()
    try:
        payload = jwt.decode(
            token,
            SETTINGS.SECRET_KEY.get_secret_value(),
            algorithms=[SETTINGS.ALGORITHM],
        )
    except JWTError:
        raise CredentialsException()

    try:
        token_content = TokenContent.model_validate_json(payload.get("sub")) #model_validate_json might not work (migrated).
    except ValidationError:
        raise CredentialsException()

    user = await get_user_instance(username=token_content.username)
    if user is None:
        raise CredentialsException()
    return user


async def get_current_user_optional_instance(
    token: str = Depends(OAUTH2_SCHEME),
):
    try:
        user = await get_current_user_instance(token)
        return user
    except HTTPException:
        return None


async def get_current_user(
    user_instance: UserModel = Depends(get_current_user_instance),
    token: str = Depends(OAUTH2_SCHEME),
):
    return User(token=token, **user_instance.model_dump())
