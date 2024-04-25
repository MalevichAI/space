from typing import Sequence, Union

from pydantic import BaseModel
from malevich_coretools import BasePlatformSettings

from .cfg import CfgSchema, LoadedCfgSchema
from .op import LoadedOpSchema, OpSchema


class SchemaAlias(BaseModel):
    src: str
    target: str


class Terminal(BaseModel):
    src: str
    target: str
    order: int | None = None


class InFlowDependency(BaseModel):
    as_collection: str | None = None
    alias: str | None = None
    reverse_id: str | None = None
    from_op_id: str | None = None
    to_op_id: str | None = None
    terminals: list[Terminal] | None = None
    schema_aliases: list[SchemaAlias] | None = None
    order: int | None = None


class InFlowAppSchema(BaseModel):
    active_op: Sequence[OpSchema] = []


class InFlowComponentSchema(BaseModel):
    reverse_id: str | None
    alias: str | None = None
    offsetX: float | None = None
    offsetY: float | None = None
    limits: BasePlatformSettings | None = None
    depends: dict[str, InFlowDependency] | None = None
    app: InFlowAppSchema | None = None
    active_cfg: Union[str, CfgSchema] | None = None


class LoadedInFlowAppSchema(InFlowAppSchema):
    app_id: str
    active_op: Sequence[LoadedOpSchema] = []


class LoadedInFlowFlowSchema(BaseModel):
    flow_id: str


class LoadedInFlowCollectionSchema(BaseModel):
    collection_id: str


class LoadedInFlowAssetSchema(BaseModel):
    asset_id: str


class LoadedPromptSchema(BaseModel):
    uid: str
    body: str
    name: str
    postcondition: str | None = None
    preconditions: list[str] | None = None


class LoadedInFlowComponentSchema(InFlowComponentSchema):
    uid: str
    comp_id: str | None = None
    reverse_id: str | None = None
    prompt: LoadedPromptSchema | None = None
    app: LoadedInFlowAppSchema | None = None
    flow: LoadedInFlowFlowSchema | None = None
    collection: LoadedInFlowCollectionSchema | None = None
    prev: list["LoadedInFlowComponentSchema"] = []
    alias: str | None = None
    active_cfg: LoadedCfgSchema | None = None
    asset: LoadedInFlowAssetSchema | None = None


class FlowSchema(BaseModel):
    is_demo: bool | None = False
    components: Sequence[InFlowComponentSchema] = []


class LoadedFlowSchema(FlowSchema):
    uid: str
    components: Sequence[LoadedInFlowComponentSchema] = []
