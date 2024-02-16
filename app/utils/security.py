from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from pydantic import BaseModel
from jose import JWTError, jwt

from ..models.user import UserModel
from ..schemas.user import User
from ..core.exceptions import CredentialsException, NotAuthenticatedException
from ..database import get_db, CouchbaseClient
from ..settings import SETTINGS


class TokenContent(BaseModel):
    username: str


PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

security = HTTPBasic()


def verify_password(plain_password, hashed_password):
    return PWD_CONTEXT.verify(plain_password, hashed_password)

def get_password_hash(password):
    return PWD_CONTEXT.hash(password)


async def get_user_instance(
    db: CouchbaseClient,
    username: str | None = None,
    email: str | None = None,
):
    """Get a user instance from its username or email"""
    if username is not None:
        query = """
            SELECT client.id,
                client.email,
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
            SELECT client.id, 
                client.email,
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
        ehrick = UserModel(**user_data)
        print(ehrick)
        return ehrick
    except Exception:
        raise CredentialsException()
    

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


async def get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    db=Depends(get_db),
):
    input_email = credentials.username #input is email even though says username (might fix later)
    input_password = credentials.password

    current_user = await authenticate_user(db, input_email, input_password)

    if current_user is None:
        raise CredentialsException()
    
    token = create_access_token(current_user)
    return User(token=token, **current_user.model_dump())


async def get_current_user_optional(
        db=(get_db),
):
    try:
        user = await get_user_instance(db=db)
        print("what on earth")
        return user
    except HTTPException:
        return None
