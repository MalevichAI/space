from abc import ABC, abstractmethod
from typing import Optional

import malevich_space.schema as schema


class BaseService(ABC):

    @abstractmethod
    def parse_raw(self, comp: schema.ComponentSchema, version_mode: schema.VersionMode, host_id: str | None = None) -> schema.LoadedComponentSchema:
        raise NotImplementedError

    @abstractmethod
    def create_host(self, alias: str, conn_url: str, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_my_hosts(self, url: Optional[str] = None, sa_core_id: Optional[str] = None, *args, **kwargs):
        raise NotImplementedError("Method not implemented")
    
    @abstractmethod
    def create_org(self, name: str, reverse_id: str) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def invite_to_org(self, reverse_id: str, members: str) -> list[str]:
        raise NotImplementedError
    
    @abstractmethod
    def create_tag(self, title: str) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def attach_tag_to_comp(self, comp_id: str, tag_ids: list[str]):
        raise NotImplementedError
    
    @abstractmethod
    def update_component(self, *args, **kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    def add_comp_to_org(self, *, comp_id: str, org_id: str) -> str | None:
        raise NotImplementedError

    @abstractmethod
    def create_component(
            self,
            name: str,
            type: str,
            description: str,
            reverse_id: str,
            repo_url: Optional[str] = None,
            designed_for: Optional[str] = None,
            not_designed_for: Optional[str] = None,
            *args, **kwargs
    ):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def create_branch(self, component_id: str, name: str, status: str, comp_rel_status: str, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def create_version(
            self,
            branch_id: str,
            readable_name: str,
            branch_version_status: str,
            updates_markdown: str,
            commit_digest: str | None,
            *args, **kwargs
    ):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def create_app_in_version(
            self,
            version_id: str,
            container_ref: Optional[str] = None,
            container_user: Optional[str] = None,
            container_token: Optional[str] = None,
            version_app_status: Optional[str] = None,
            *args, **kwargs
    ):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_flow_by_version_id(self, version_id: str) -> str | None:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def create_flow_in_version(
            self,
            version_id: str,
            is_demo: Optional[bool] = None,
            version_flow: Optional[str] = None,
            *args, **kwargs
    ):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def create_collection(
            self,
            host_id: str,
            core_id: Optional[str] = None,
            core_alias: Optional[str] = None,
            schema_core_id: Optional[str] = None,
            org_id: Optional[str] = None,
            *args, **kwargs
    ):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def create_collection_in_version(
            self,
            version_id: str,
            ca_id: str,
            version_ca_status: Optional[str] = None,
            *args, **kwargs
    ):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_branch_by_name(self, component_id: str, branch_name: str, *args, **kwargs) -> schema.LoadedBranchSchema | None:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def add_comp_in_flow(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def add_ca_to_comp_flow(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def link(self, *args, **kwargs) -> str | None:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def create_cfg_standalone(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def create_scheme(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def create_op(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def add_op_2_av(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def select_active_op(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def set_in_flow_component_cfg(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_schema(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def add_cfg_2_av(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def add_dep_2_op(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_component_by_reverse_id(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def build_task(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def boot_task(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def change_task_state(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def update_ca(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def run_task(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def add_schema_alias(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def create_use_case(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def attach_use_case(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def org_id(self) -> str | None:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_parsed_component_by_reverse_id(self, reverse_id: str) -> schema.LoadedComponentSchema | None:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def wipe_component(self, uid: Optional[str] = None, reverse_id: Optional[str] = None) -> bool:
        raise NotImplementedError

    @abstractmethod
    def create_endpoint(self, task_id: str, alias: str | None, token: str | None) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def create_asset(
            self,
            *,
            asset: schema.CreateAsset,
            host_id: str | None = None
    ) -> schema.Asset:
        raise NotImplementedError
    
    @abstractmethod
    def create_asset_in_version(
            self,
            *,
            version_id: str,
            asset: schema.CreateAsset,
            host_id: str | None = None
    ) -> schema.Asset:
        raise NotImplementedError
    
    @abstractmethod
    def auto_layout(self, *, flow: str):
        raise NotImplementedError
    
    @abstractmethod
    def get_task_core_id(self, *, task_id: str) -> tuple[str, str]:
        raise NotImplementedError

    @abstractmethod
    def get_deployments_by_reverse_id(self, *, reverse_id: str) -> list[schema.LoadedTaskSchema]:
        raise NotImplementedError
