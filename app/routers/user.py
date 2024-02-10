from fastapi import APIRouter, Body, Depends, HTTPException
from couchbase.exceptions import DocumentExistsException, CouchbaseException

from ..schemas.user import LoginUser, NewUser, UpdateUser, User, UserResponse
from ..models.user import UserModel
from ..database import get_db
from ..utils.security import (
    OAUTH2_SCHEME,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_current_user_instance,
    get_password_hash,
)


router = APIRouter(
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


USER_COLLECTION = "user"


@router.post(
    "/users/login",
    response_model=UserResponse,
    description="Authenticate user. \n\n Method: `user_auth`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def user_auth(
    user_input: LoginUser = Body(..., embed=True, alias="user"),
):
    # Need to implement response return
    return {"POST user authentication" : "Returns a User"}


@router.post(
    "/users/",
    response_model=UserResponse,
    description="Register user. \n\n Method: `user_reg`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def user_reg(
    user: NewUser = Body(..., embed=True),
    db=Depends(get_db),
):
    instance = UserModel(
        **user.model_dump(), hashed_password=get_password_hash(user.password)
    )
    try:
        db.insert_document(USER_COLLECTION, instance.username, instance.model_dump())
    except DocumentExistsException:
        raise HTTPException(status_code=409, detail="Article already exists")
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except CouchbaseException:
        raise HTTPException()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    token = create_access_token(instance)
    return UserResponse(user=User(token=token, **user.model_dump()))


@router.get(
    "/user",
    response_model=UserResponse,
    description="Get the current user. \n\n Method: `current_user`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def current_user(
    current_user: User = Depends(get_current_user),
):
    # Need to implement response return
    return {"GET current user " : "Returns a User that is the current user"}


@router.put(
    "/user",
    response_model=UserResponse,
    description="Update the current user. \n\n Method: `update_user`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def update_user(
    update_user: UpdateUser = Body(..., embed=True, alias="user"),
    user_instance: User = Depends(get_current_user_instance),
    token: str = Depends(OAUTH2_SCHEME),
):
    # Need to implement response return
    return {"PUT update user" : "Returns a User"}