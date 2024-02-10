from datetime import datetime
from typing import List, Sequence

from pydantic import Field

from models.article import ArticleModel
from models.user import UserModel
from schemas.user import Profile

from .base import BaseSchema


class Article(BaseSchema):
    slug: str
    title: str
    description: str
    body: str
    tag_list: List[str] = Field(..., alias="tagList")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    favorited: bool = False
    favorites_count: int = Field(0, alias="favoritesCount")
    author: Profile

    @classmethod
    def from_article_instance(
        cls, article: ArticleModel, user: UserModel | None = None
    ) -> "Article":
        if user is None:
            favorited = False
        else:
            favorited = user.id in article.favorited_user_ids

        return cls(
            favorited=favorited,
            favorites_count=len(article.favorited_user_ids),
            **article.model_dump()
        )


class SingleArticleResponse(BaseSchema):
    article: Article

    @classmethod
    def from_article_instance(
        cls, article: ArticleModel, user: UserModel | None = None
    ) -> "SingleArticleResponse":
        return cls(article=Article.from_article_instance(article=article, user=user))


class MultipleArticlesResponse(BaseSchema):
    articles: List[Article]
    articles_count: int = Field(..., alias="articlesCount")

    @classmethod
    def from_article_instances(
        cls,
        articles: Sequence[ArticleModel],
        total_count: int,
        user: UserModel | None = None,
    ) -> "MultipleArticlesResponse":
        articles = [Article.from_article_instance(a, user) for a in articles]
        return cls(articles=articles, articles_count=total_count)
    

class NewArticle(BaseSchema):
    title: str
    description: str
    body: str
    tag_list: List[str] | None = Field(None, alias="tagList")


class UpdateArticle(BaseSchema):
    title: str | None = None
    description: str | None = None
    body: str | None = None
