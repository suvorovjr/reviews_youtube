from typing import List

from pydantic import BaseModel, Field


class PageInfoModel(BaseModel):
    total_results: int = Field(alias='totalResults')


class IdModel(BaseModel):
    kind: str
    channelId: str


class ItemModel(BaseModel):
    kind: str
    id: IdModel


class ChanelIDResponseModel(BaseModel):
    page_info: PageInfoModel = Field(alias='pageInfo')
    items: List[ItemModel]
