from fastapi import APIRouter, Depends, HTTPException

from ..core.user import query_users_by_username
from ..database import get_db
from ..models.user import UserModel
from ..schemas.user import ProfileWrapperSchema, ProfileResponseSchema
from ..utils.security import get_current_user_optional_instance, get_current_user_instance

from .user import USER_COLLECTION


router = APIRouter()


@router.get(
    "/profiles/{username}",
    response_model=ProfileWrapperSchema
)
async def get_profile(
    username: str,
    logged_user: UserModel | None = Depends(get_current_user_optional_instance),
    db=Depends(get_db)
):
    user = await query_users_by_username(username, db)
    following = False
    if logged_user is not None and user.id in logged_user.following_ids:
        following = True
    return ProfileWrapperSchema(profile=ProfileResponseSchema(following=following, **user.model_dump()))


@router.post(
    "/profiles/{username}/follow",
    response_model=ProfileWrapperSchema)
async def follow_user(
    username: str,
    user_instance: UserModel = Depends(get_current_user_instance),
    db=Depends(get_db)
):
    user_to_follow = await query_users_by_username(username, db)
    following_set = set(user_instance.following_ids) | set((user_to_follow.id,))
    user_instance.following_ids = tuple(following_set)
    try:
        db.upsert_document(USER_COLLECTION, user_instance.id, user_instance.model_dump())
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    
    profile = ProfileResponseSchema(following=True, **user_to_follow.model_dump())
    return ProfileWrapperSchema(profile=profile)


@router.delete(
    "/profiles/{username}/follow",
    response_model=ProfileWrapperSchema)
async def unfollow_user(
    username: str,
    user_instance: UserModel = Depends(get_current_user_instance),
    db=Depends(get_db)
):
    user_to_unfollow = await query_users_by_username(username, db)
    following_set = set(user_instance.following_ids) - set((user_to_unfollow.id,))
    user_instance.following_ids = tuple(following_set)
    try:
        db.upsert_document(USER_COLLECTION, user_instance.id, user_instance.model_dump())
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    
    profile = ProfileResponseSchema(following=False, **user_to_unfollow.model_dump())
    return ProfileWrapperSchema(profile=profile)
