from contextlib import asynccontextmanager
from fastapi import FastAPI

from .database import get_db
from .routers.article import router as article_router
from .routers.comment import router as comment_router
from .routers.profile import router as profile_router
from .routers.tag import router as tag_router
from .routers.user import router as user_router


# Initialize couchbase connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Method that gets called upon app initialization to initialize couchbase connection & close the connection on exit"""
    db = get_db()
    yield
    db.close()


api = FastAPI(
    title="Couchbase FastAPI RealWorld",
    version="1.0.0",
    description="""
    RealWorld backend built with FastAPI and Couchbase Capella.
    """,
    lifespan=lifespan,
)


api.include_router(article_router, tags=["articles"], prefix="/api")
api.include_router(comment_router, tags=["comments"], prefix="/api")
api.include_router(profile_router, tags=["profiles"], prefix="/api")
api.include_router(tag_router, tags=["tags"], prefix="/api")
api.include_router(user_router, tags=["users"], prefix="/api")
