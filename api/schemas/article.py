from datetime import datetime
from typing import List

from .base import BaseSchema
from ..models.article import ArticleModel
from ..models.user import UserModel
from .user import ProfileResponseSchema


class CreateArticleSchema(BaseSchema):
    title: str
    description: str
    body: str
    tagList: List[str] | None = None


class UpdateArticleSchema(BaseSchema):
    title: str | None = None
    description: str | None = None
    body: str | None = None


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
            favorited = user.id in article.favoritedUserIds

        return cls(
            favorited=favorited,
            favoritesCount=len(article.favoritedUserIds),
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

    @classmethod
    def from_article_instances(
        cls,
        articles: List[ArticleModel],
        total_count: int,
        user: UserModel | None = None,
    ) -> "MultipleArticlesWrapperSchema":
        articles = [ArticleResponseSchema.from_article_instance(a, user) for a in articles]
        return cls(articles=articles, articlesCount=total_count)
