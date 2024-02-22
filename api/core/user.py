from fastapi import HTTPException

from ..models.user import UserModel
from .exceptions import UserNotFoundException


async def query_users_db(
    db,
    id: str | None = None,
    username: str | None = None,
) -> UserModel:
    """Query db for user instance by ID or username and returns instance."""
    if id is not None:
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
    elif username is not None:
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
    else:
        raise HTTPException(status_code=422, details="No id or username provided")
    if query is None:
        raise UserNotFoundException()
    try:
        queryResult = db.query(query, id=id, username=username)
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
