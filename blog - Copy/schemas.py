from typing import List
from pydantic import BaseModel

class Tag(BaseModel):
    name: str
    group_id: int
    class Config():
        orm_mode = True

class TagGroup(BaseModel):
    name: str

class ShowTagGroup(Tag):
    name: str
    tags: List[Tag] = []
    class Config():
        orm_mode = True

class ShowTag(Tag):
    name: str
    group: ShowTagGroup
    class Config():
        orm_mode = True