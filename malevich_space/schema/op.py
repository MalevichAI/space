from typing import Sequence, Optional

from pydantic import BaseModel

from .dep import DepSchema, LoadedDepSchema
from .schema import LoadedSchemaSchema


class OpArg(BaseModel):
    arg_name: Optional[str]
    arg_type: Optional[str]
    arg_order: Optional[int]


class OpSchema(BaseModel):
    core_id: str | None = None
    type: str | None = None

    requires: Sequence[DepSchema] = []


class LoadedOpSchema(OpSchema):
    uid: str
    name: Optional[str] = None
    doc: Optional[str] = None
    finish_msg: Optional[str] = None

    tl: Optional[int] = None
    query: Optional[str] = None
    mode: Optional[str] = None

    collections_names: Optional[list[str]]  = None
    extra_collections_names: Optional[list[str]] = None

    collection_out_names: Optional[list[str]] = None

    args: Optional[list[OpArg]] = None

    input_schema: Sequence[LoadedSchemaSchema] = []
    output_schema: Sequence[LoadedSchemaSchema] = []
    loaded_requires: Sequence[LoadedDepSchema] = []
