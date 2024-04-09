from typing import Dict, Any

from pydantic import BaseModel


class CfgSchema(BaseModel):
    readable_name: str | None = None
    core_name: str | None = None
    cfg_json: Dict[str, Any] | None = None
    core_id: str | None = None


class LoadedCfgSchema(CfgSchema):
    uid: str
