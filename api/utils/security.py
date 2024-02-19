from datetime import datetime, timedelta
from jose import jwt, JWTError
import json
from pydantic import BaseModel, ValidationError
from typing import cast
from fastapi import FastAPI, Depends, HTTPException

from passlib.context import CryptContext
from fastapi.openapi.models import OAuthFlows
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request

from ..core.exceptions import NotAuthenticatedException, CredentialsException
from ..database import get_db
from ..models.user import UserModel
from ..schemas.user import UserResponseSchema
from ..settings import SETTINGS


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenContent(BaseModel):
    username: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class OAuth2PasswordToken(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str | None = None,
        scopes: dict | None = None,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlows(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=False)

    async def __call__(self, request: Request) -> str | None:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "token":
            return None
        return cast(str, param)
    

OAUTH2_SCHEME = OAuth2PasswordToken(tokenUrl="/users")


api = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def query_db_for_user(
    db,
    email: str | None = None,
    username: str | None = None
):
    if username is not None:
        query = """
            SELECT client.id,
                client.email,
                client.username,
                client.bio,
                client.image,
                client.hashed_password
            FROM client as client 
            WHERE client.username=$username;
        """
    elif email is not None:
        query = """
            SELECT client.id, 
                client.email,
                client.username,
                client.bio,
                client.image,
                client.hashed_password
            FROM client as client 
            WHERE client.email=$email;
        """
    else:
        return None

    queryResult = db.query(query, email=email, username=username)
    user_data = [r for r in queryResult][0]
    return UserModel(**user_data)


async def authenticate_user(email: str, password: str, db):
    user = await query_db_for_user(db, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def create_access_token(user: UserModel) -> str:
    token_content = TokenContent(username=user.username)
    expire = datetime.utcnow() + timedelta(minutes=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": token_content.model_dump_json()}
    encoded_jwt = jwt.encode(
        to_encode, SETTINGS.SECRET_KEY.get_secret_value(), algorithm=SETTINGS.ALGORITHM
    )
    return str(encoded_jwt)


async def get_current_user_instance(
    db=Depends(get_db),
    token: str | None = Depends(OAUTH2_SCHEME),
) -> UserModel:
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
        payload_model = json.loads(payload.get("sub"))
        token_content = TokenContent(**payload_model)

    except ValidationError:
        raise CredentialsException()

    user = await query_db_for_user(db, username=token_content.username)
    if user is None:
        raise CredentialsException()
    return user


async def get_current_user_optional_instance(
    db=Depends(get_db),
    token: str = Depends(OAUTH2_SCHEME),
) -> UserModel | None:
    try:
        user = await get_current_user_instance(db, token)
        return user
    except HTTPException:
        return None


async def get_current_user(
    user_instance: UserModel = Depends(get_current_user_instance),
    token: str = Depends(OAUTH2_SCHEME),
) -> UserResponseSchema:
    return UserResponseSchema(token=token, **user_instance.model_dump())
