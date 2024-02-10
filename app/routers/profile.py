from fastapi import APIRouter, status, Depends

from ..models.user import UserModel
from ..schemas.user import Profile, ProfileResponse
from ..utils.security import get_current_user_instance, get_current_user_optional_instance


router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{username}",
    response_model=ProfileResponse,
    description="Get a single profile. \n\n Method: `get_profile`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def get_profile(
    username: str,
    logged_user: UserModel | None = Depends(get_current_user_optional_instance),
):
    # Need to implement response return
    return {"GET profile" : "Returns a Profile"}


@router.post(
    "/{username}/follow",
    response_model=ProfileResponse,
    description="Follow a single profile. \n\n Method: `follow_profile`",
    status_code=status.HTTP_201_CREATED,
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def follow_profile(
    username: str,
    user_instance: UserModel = Depends(get_current_user_instance),
):
    # Need to implement response return
    return {"POST follow profile" : "Returns a Profile"}


@router.delete(
    "/{username}/follow",
    response_model=ProfileResponse,
    description="Unfollow a single profile. \n\n Method: `unfollow_profile`",
    status_code=status.HTTP_200_OK,
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def unfollow_profile(
    username: str,
    user_instance: UserModel = Depends(get_current_user_instance),
):
    # Need to implement response return
    return {"DELETE unfollow profile" : "Returns a Profile"}