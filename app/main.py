from fastapi import FastAPI

from .internal import admin
from .routers import article, comment, profile, tag, user


app = FastAPI()


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