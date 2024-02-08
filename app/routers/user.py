from fastapi import APIRouter

router = APIRouter(
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/users/login", tags=["users"])
async def user_auth():
    #TBC
    return {"POST user authentication" : "Returns a User"}


@router.post("/users/", tags=["users"])
async def user_reg():
    #TBC
    return {"POST user registration" : "Returns a User"}


@router.get("/user", tags=["users"])
async def current_user():
    #TBC
    return {"GET current user " : "Returns a User that is the current user"}


@router.put("/user", tags=["users"])
async def update_user():
    #TBC
    return {"PUT update user" : "Returns a User"}