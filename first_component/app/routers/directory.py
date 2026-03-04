from fastapi import APIRouter, HTTPException, Depends
import os

from app.directory.models import (
    FileRequest,
    DirectoryRouterResponse,
    FileListResponse,
)
from app.directory.utils import (
    grab_base_dir,
    check_fpath_is_valid,
    check_file_exists,
    write_to_file,
    check_content_valid,
)

router = APIRouter(prefix="/directory", tags=["directory"])

@router.post("/create")
async def create(request: FileRequest, base_dir: str = Depends(grab_base_dir)) -> DirectoryRouterResponse:
    target_path = check_fpath_is_valid(base_dir, request.path)

    if os.path.isfile(target_path):
        raise HTTPException(status_code=409, detail="File already exists")

    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    content = check_content_valid(request.content)
    write_to_file(target_path, content)
    return DirectoryRouterResponse(message="File created", path=request.path)

@router.post("/update")
async def update(request: FileRequest, base_dir: str = Depends(grab_base_dir)) -> DirectoryRouterResponse:
    target_path = check_fpath_is_valid(base_dir, request.path)

    check_file_exists(target_path)
    content = check_content_valid(request.content)
    write_to_file(target_path, content)

    return DirectoryRouterResponse(message="File updated", path=request.path)

@router.post("/delete")
async def delete(request: FileRequest, base_dir: str = Depends(grab_base_dir)) -> DirectoryRouterResponse:
    target_path = check_fpath_is_valid(base_dir, request.path)
    check_file_exists(target_path)
    os.remove(target_path)
    return DirectoryRouterResponse(message="File deleted", path=request.path)

@router.post("/list")
def list(base_dir: str = Depends(grab_base_dir)) -> FileListResponse:
    if base_dir is None:
        raise HTTPException(status_code=403, detail="No base directory currently specified")
    return FileListResponse(files=[f for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f))])