from fastapi import APIRouter, Body, Depends

from ..schemas.user import LoginUser, NewUser, UpdateUser, User, UserResponse
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
):
    # Need to implement response return
    return {"POST user registration" : "Returns a User"}


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