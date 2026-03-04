from pydantic import BaseModel
from typing import Optional

class FileRequest(BaseModel):
    path: str
    content: Optional[str] = None

class DirectoryRouterResponse(BaseModel):
    message: str
    path: str

class FileListResponse(BaseModel):
    files: list[str]