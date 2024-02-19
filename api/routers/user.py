from couchbase.exceptions import DocumentExistsException
from fastapi import APIRouter, Body, Depends, HTTPException

from ..core.exceptions import InvalidCredentialsException
from ..database import get_db
from ..models.user import UserModel
from ..schemas.user import (
    AuthenticationRequestSchema,
    RegistrationRequestSchema,
    UpdateUserSchema,
    UserResponseSchema,
    UserWrapperSchema
)
from ..utils.security import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_current_user_instance,
    get_password_hash,
    OAUTH2_SCHEME
)


router = APIRouter(
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


USER_COLLECTION = "client"


@router.post(
    "/users",
    response_model=UserWrapperSchema
)
async def register(
    user: RegistrationRequestSchema = Body(..., embed=True),
    db=Depends(get_db)
):
    print(user)
    user_model = UserModel(
        **user.model_dump(),
        hashed_password=get_password_hash(user.password))

    try:
        db.insert_document(USER_COLLECTION, user_model.id, user_model.model_dump())
    except DocumentExistsException:
        raise HTTPException(status_code=409, detail="User already exists")
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    
    token = await create_access_token(user_model)

    response_user = UserResponseSchema(token=token, **user_model.model_dump())
    return UserWrapperSchema(user=response_user)


@router.post(
    "/users/login",
    response_model=UserWrapperSchema
)
async def login_user(
    user: AuthenticationRequestSchema = Body(..., embed=True),
    db=Depends(get_db)
):
    user = await authenticate_user(
        user.email, user.password.get_secret_value(), db
    )
    if user is None:
        raise InvalidCredentialsException()

    token = await create_access_token(user)

    response_user = UserResponseSchema(token=token, **user.model_dump())
    return UserWrapperSchema(user = response_user)


@router.get(
    "/user",
    response_model=UserWrapperSchema)
async def current_user(
    current_user: UserResponseSchema = Depends(get_current_user),
):
    return UserWrapperSchema(user=current_user)


@router.put(
    "/user",
    response_model=UserWrapperSchema
)
async def update_user(
    user: UpdateUserSchema = Body(..., embed=True),
    user_instance: UserModel = Depends(get_current_user_instance),
    token: str = Depends(OAUTH2_SCHEME),
    db=Depends(get_db)
):
    patch_dict = user.model_dump(exclude_unset=True)
    for name, value in patch_dict.items():
        setattr(user_instance, name, value)

    try:
        db.upsert_document(USER_COLLECTION, user_instance.id, user_instance.model_dump())
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    response_user = UserResponseSchema(token=token, **user_instance.model_dump())
    return UserWrapperSchema(user=response_user)
