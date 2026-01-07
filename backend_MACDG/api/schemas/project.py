from pydantic import BaseModel
from typing import List

class ProjectCreateRequest(BaseModel):
    repo_url: str
    personas: List[str]
    # user_id: int

class ProjectInitResponse(BaseModel):
    project_id: str
    personas: List[str]
