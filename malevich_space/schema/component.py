from enum import Enum

from typing import Optional, Sequence

from pydantic import BaseModel

from .branch import BranchSchema, LoadedBranchSchema
from .cfg import CfgSchema, LoadedCfgSchema
from .collection_alias import CollectionAliasSchema, LoadedCollectionAliasSchema
from .flow import FlowSchema, LoadedFlowSchema
from .op import LoadedOpSchema, OpSchema
from .schema import SchemaMetadata
from .version import LoadedVersionSchema, VersionSchema
from .asset import Asset


class AppSchema(BaseModel):
    uid: str | None = None
    container_ref: str | None = None
    container_user: str | None = None
    container_token: str | None = None

    preload_ops: bool = True

    ops: Sequence[OpSchema] = []
    cfg: Sequence[CfgSchema] = []


class LoadedAppSchema(AppSchema):
    uid: str
    ops: Sequence[LoadedOpSchema] = []
    cfg: Sequence[LoadedCfgSchema] = []


class UseCaseSchema(BaseModel):
    title: str | None = None
    body: str | None = None

    is_public_example: bool | None = False


class ComponentType(Enum):
    APP = "app"
    FLOW = "flow"
    COLLECTION = "collection"
    ASSET = "asset"


class ComponentSchema(BaseModel):
    name: str
    reverse_id: str
    uid: str | None = None

    visibility: list[str] = []

    anticipated_python_deps: list[str] = []
    anticipated_default: list[str] = []
    anticipated_api_call: str | None = None
    anticipated_api_name: str | None = None

    example_code_before_juliusfication: str | None = None

    description: str | None = None
    designed_for: str | None = None
    not_designed_for: str | None = None

    designed_for_use_case: list[UseCaseSchema] = []
    not_designed_for_use_case: list[UseCaseSchema] = []

    tags: list[str] | None = None

    app: AppSchema | None = None
    flow: FlowSchema | None = None
    collection: CollectionAliasSchema | None = None
    asset: Asset | None = None

    icon: str | None = None
    hf_url: str | None = None
    repo_url: str | None = None
    docs_url: str | None = None

    branch: BranchSchema | None = None
    version: VersionSchema | None = None

    required_schema: list[SchemaMetadata] = []

    def load(self, sops) -> Optional["LoadedComponentSchema"]:
        return sops.get_parsed_component_by_reverse_id(reverse_id=self.reverse_id)

    def is_type(self, type_in: ComponentType | str) -> bool:
        if type(type_in) == str:
            type_in = ComponentType(type_in)
        if type_in == ComponentType.APP:
            return self.app is not None
        elif type_in == ComponentType.FLOW:
            return self.flow is not None
        elif type_in == ComponentType.COLLECTION:
            return self.collection is not None
        elif type_in == ComponentType.ASSET:
            return self.asset is not None
        return False

    def type(self) -> ComponentType:
        if self.app:
            return ComponentType.APP
        elif self.flow:
            return ComponentType.FLOW
        elif self.collection:
            return ComponentType.COLLECTION
        elif self.asset:
            return ComponentType.ASSET
        raise TypeError("Unknown component type")

    def __str__(self) -> str:
        return f"<uid={self.uid}, reverseId={self.reverse_id}, type={self.type()}>"


class LoadedComponentSchema(ComponentSchema):
    uid: str

    branch: LoadedBranchSchema | None = None
    version: LoadedVersionSchema | None = None

    app: LoadedAppSchema | None = None
    flow: LoadedFlowSchema | None = None
    collection: LoadedCollectionAliasSchema | None = None
