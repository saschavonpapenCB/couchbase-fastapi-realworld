from fastapi import APIRouter

router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{username}")
async def get_profile():
    #TBC
    return {"GET profile" : "Returns a Profile"}


@router.post("/{username}/follow")
async def follow_profile():
    #TBC
    return {"POST follow profile" : "Returns a Profile"}


@router.delete("/{username}/follow")
async def unfollow_profile():
    #TBC
    return {"DELETE unfollow profile" : "Returns a Profile"}