from pydantic import BaseModel
import tomllib

class Config(BaseModel):
    BASE_DIR: str
    MAX_FILE_SIZE: int

def load_config() -> Config:
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    return Config(**config)

config = load_config()