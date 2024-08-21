import json
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field


class PageInfoModel(BaseModel):
    total_results: int = Field(alias='totalResults')
    result_per_page: int = Field(alias='resultsPerPage')


class IdModel(BaseModel):
    kind: str
    channel_id: str = Field(alias='channelId', default=None)
    video_id: str = Field(alias='videoId', default=None)


class ItemModel(BaseModel):
    kind: str
    id: IdModel


class ChanelIDResponseModel(BaseModel):
    page_info: PageInfoModel = Field(alias='pageInfo')
    items: List[ItemModel]


class SnippetModel(BaseModel):
    published_at: datetime = Field(alias='publishedAt')
    title: str


class VideoModel(BaseModel):
    kind: str
    id: IdModel
    snippet: SnippetModel


class VideosListModel(BaseModel):
    next_page_token: str = Field(alias='nextPageToken', default=None)
    page_info: PageInfoModel = Field(alias='pageInfo')
    videos: List[VideoModel] = Field(alias='items')


class TopLevelSnippetModel(BaseModel):
    chanel_id: str = Field(alias='channelId')
    video_id: str = Field(alias='videoId')
    review_text: str = Field(alias='textDisplay')
    original_text_review: str = Field(alias='textOriginal')
    author_name: str = Field(alias='authorDisplayName')
    like_count: int = Field(alias='likeCount')
    published_at: datetime = Field(alias='publishedAt')
    updated_at: datetime = Field(alias='updatedAt')


class TopLevelCommentModel(BaseModel):
    kind: str
    id: str
    snippet: TopLevelSnippetModel


class ReviewSnippetModel(BaseModel):
    topLevelComment: TopLevelCommentModel


class ReviewModel(BaseModel):
    kind: str
    id: str
    snippet: ReviewSnippetModel


class ReviewsResponseModel(BaseModel):
    page_info: PageInfoModel = Field(alias='pageInfo')
    items: List[ReviewModel]
