import base64
from fastapi import HTTPException
import os

from app.config import config

def grab_base_dir() -> str:
    if config.BASE_DIR is None:
        raise HTTPException(status_code=403, detail="No base directory currently specified")
    return config.BASE_DIR

def check_fpath_is_valid(base_dir: str, fpath: str) -> str:
    """
    Validates whether `fpath` is a valid relative path within `base_dir`.
    Provides the absolute path if all checks pass.
    """
    if os.path.isabs(fpath):
        raise HTTPException(status_code=400, detail="Absolute paths are not allowed")

    fpath = os.path.normpath(fpath)
    if fpath.startswith(".."):
        raise HTTPException(status_code=400, detail="Relative path escapes base directory")

    base_realpath = os.path.realpath(base_dir)
    target_realpath = os.path.realpath(os.path.join(base_dir, fpath))
    if os.path.commonpath([base_realpath, target_realpath]) != base_realpath:
        raise HTTPException(status_code=400, detail="Invalid file path")
    return target_realpath

def check_file_exists(fpath: str):
    if not os.path.exists(fpath) or not os.path.isfile(fpath):
        raise HTTPException(status_code=404, detail="File not found")

def write_to_file(fpath: str, content: bytes):
    with open(fpath, "wb") as f:
        f.write(content)

def check_content_valid(content: str) -> bytes:
    """
    Validates the content of the file we are creating or updating.
    Returns a decoded form of the content if all checks pass.
    """
    if content is None:
        return b""
    try:
        decoded_content = base64.b64decode(content, validate=True)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 content")

    if len(decoded_content) > config.MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")
    return decoded_content