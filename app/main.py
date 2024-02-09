from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware

from .internal import admin
from .routers import article, comment, profile, tag, user
from .database import get_db


# Initialize couchbase connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Method that gets called upon app initialization to initialize couchbase connection & close the connection on exit"""
    db = get_db()
    yield
    db.close()


app = FastAPI(
    title="Couchbase FastAPI RealWorld",
    version="1.0.0",
    description="""
    RealWorld backend built with FastAPI and Couchbase Capella.
    """,
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(article.router)
app.include_router(comment.router)
app.include_router(profile.router)
app.include_router(tag.router)
app.include_router(user.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    responses={418: {"Admin": "Returns the website admin"}},
)


@app.get("/")
async def root():
    return {"GET website root": "Returns the website root"}