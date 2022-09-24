from typing import List, Union
from pydantic import BaseModel

class Tag(BaseModel):
    name: str
    description: str = None
    class Config():
        orm_mode = True

class TagGroup(BaseModel):
    name: str
    description: str = None

class ShowTagGroup(Tag):
    name: str
    description: str = None
    tags: List[Tag] = []
    class Config():
        orm_mode = True

class ShowTag(Tag):
    name: str
    description: str = None
    group: ShowTagGroup
    class Config():
        orm_mode = True

class Project(BaseModel):
    name: str
    description: str
    region: str