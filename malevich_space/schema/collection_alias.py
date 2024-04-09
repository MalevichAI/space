from pydantic import BaseModel


class CollectionAliasSchema(BaseModel):
    core_alias: str | None = None
    path: str | None = None
    core_id: str | None = None
    schema_core_id: str | None = None
    docs: list[str] | None = None


class LoadedCollectionAliasSchema(CollectionAliasSchema):
    uid: str
