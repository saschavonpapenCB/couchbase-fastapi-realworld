from datetime import datetime
from typing import List

from .base import BaseSchema
from ..models.article import ArticleModel
from ..models.user import UserModel
from .user import ProfileResponseSchema


class CreateArticleRequestSchema(BaseSchema):
    title: str
    description: str
    body: str
    tagList: List[str] | None = None


class ArticleResponseSchema(BaseSchema):
    slug: str
    title: str
    description: str
    body: str
    tagList: List[str]
    createdAt: datetime
    updatedAt: datetime
    favorited: bool = False
    favoritesCount: int = 0
    author: ProfileResponseSchema

    @classmethod
    def from_article_instance(
        cls, article: ArticleModel, user: UserModel | None = None
    ) -> "ArticleResponseSchema":
        if user is None:
            favorited = False
        else:
            favorited = user.identifier in article.favoritedUserIds

        return cls(
            favorited=favorited,
            favorites_count=len(article.favoritedUserIds),
            **article.model_dump()
        )


class ArticleWrapperSchema(BaseSchema):
    article: ArticleResponseSchema

    @classmethod
    def from_article_instance(
        cls, article: ArticleModel, user: UserModel | None = None
    ) -> "ArticleWrapperSchema":
        return cls(article=ArticleResponseSchema.from_article_instance(article=article, user=user))


class MultipleArticlesWrapperSchema(BaseSchema):
    articles: List[ArticleResponseSchema]
    articlesCount: int = 0
