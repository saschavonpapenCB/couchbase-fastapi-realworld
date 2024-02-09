from fastapi import APIRouter, status
from ..models.user import ProfileModel

router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{username}",
    response_model=ProfileModel,
    description="Get a single profile. \n\n Method: `get_profile`",
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def get_profile() -> ProfileModel:
    # Need to implement response return
    return {"GET profile" : "Returns a Profile"}


@router.post(
    "/{username}/follow",
    response_model=ProfileModel,
    description="Follow a single profile. \n\n Method: `follow_profile`",
    status_code=status.HTTP_201_CREATED,
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def follow_profile() -> ProfileModel:
    # Need to implement response return
    return {"POST follow profile" : "Returns a Profile"}


@router.delete(
    "/{username}/follow",
    response_model=ProfileModel,
    description="Unfollow a single profile. \n\n Method: `unfollow_profile`",
    status_code=status.HTTP_200_OK,
    responses={
        500: {
            "description": "Unexpected Error",
        },
    },
)
async def unfollow_profile() -> ProfileModel:
    # Need to implement response return
    return {"DELETE unfollow profile" : "Returns a Profile"}