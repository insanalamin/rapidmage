from typing import List

from pydantic.main import BaseModel


class SharedConfiguration(BaseModel):
    registered_repositories: List[str] = [] 
