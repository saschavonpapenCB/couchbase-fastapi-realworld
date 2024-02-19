from fastapi import HTTPException

from .exceptions import UserNotFoundException
from ..models.user import UserModel


async def query_users_by_id(
        id: str,
        db
) -> UserModel:
    query = """
        SELECT client.id,
                client.email,
                client.username,
                client.bio,
                client.image,
                client.hashed_password
            FROM client as client 
            WHERE client.id=$id;
    """
    try:
        queryResult = db.query(query, id=id)
        response_data = [r for r in queryResult]
        if not response_data:
            raise UserNotFoundException()
        else:
            response_user = response_data[0]
            return UserModel(**response_user)
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    

async def query_users_by_username(
        username: str,
        db
) -> UserModel:
    query = """
        SELECT client.id,
                client.email,
                client.username,
                client.bio,
                client.image,
                client.hashed_password
            FROM client as client 
            WHERE client.username=$username;
    """
    try:
        queryResult = db.query(query, username=username)
        response_data = [r for r in queryResult]
        if not response_data:
            raise UserNotFoundException()
        else:
            response_user = response_data[0]
            return UserModel(**response_user)
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
