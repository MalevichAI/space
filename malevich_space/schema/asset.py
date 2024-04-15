import re

from pydantic import BaseModel, Field


class CreateAsset(BaseModel):
    core_path: str
    is_composite: bool | None = None
    checksum: str | None = None


class Asset(CreateAsset):
    uid: str | None = None
    upload_url: str | None = None
    download_url: str | None = None
