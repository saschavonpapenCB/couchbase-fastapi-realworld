from fastapi import APIRouter
from ..models.user import UserModel


router = APIRouter(
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/users/login",
    response_model=UserModel,
    description="Authenticate user. \n\n Method: `user_auth`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def user_auth() -> UserModel:
    #TBC
    return {"POST user authentication" : "Returns a User"}


@router.post(
    "/users/",
    response_model=UserModel,
    description="Register user. \n\n Method: `user_reg`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def user_reg() -> UserModel:
    #TBC
    return {"POST user registration" : "Returns a User"}


@router.get(
    "/user",
    response_model=UserModel,
    description="Get the current user. \n\n Method: `current_user`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def current_user() -> UserModel:
    #TBC
    return {"GET current user " : "Returns a User that is the current user"}


@router.put(
    "/user",
    response_model=UserModel,
    description="Update the current user. \n\n Method: `update_user`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def update_user() -> UserModel:
    #TBC
    return {"PUT update user" : "Returns a User"}