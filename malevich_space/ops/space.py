from typing import Any, Iterable, Optional, Union, overload

import json
import requests

from gql import Client
from gql.transport.requests import RequestsHTTPTransport
from gql.transport.websockets import WebsocketsTransport
from graphql import DocumentNode, ExecutionResult

import malevich_space.gql as client
import malevich_space.schema as schema
from ..schema.flow import LoadedInFlowCollectionSchema, LoadedOpSchema

from .service import BaseService


class SpaceOps(BaseService):
    def __init__(self, space_setup: schema.SpaceSetup) -> None:
        self.space_setup = space_setup
        self.token = self.auth(self.space_setup.username, self.space_setup.password)
        self.client, self.ws_client = self.init_graphql()
        self.org = self.get_org(reverse_id=self.space_setup.org)

    def parse_raw(self, comp: schema.ComponentSchema, version_mode: schema.VersionMode, host_id: str | None = None, sync: bool = True) -> schema.LoadedComponentSchema | str:
        raw = comp.model_dump_json()
        result = self._org_request(client.parse_raw_component, variable_values={
            "raw_component": raw,
            "version_mode": version_mode.value,
            "host_id": host_id,
            "sync": sync
        })
        if sync:
            return self._parse_comp(result["components"]["createFromJson"])
        return result["components"]["createFromJson"]["id"]

    def org_id(self) -> str | None:
        if self.org:
            return self.org.uid
        return None

    def _org_request(
            self,
            request: DocumentNode,
            variable_values: Optional[dict[str, Any]] = None
    ) -> Union[dict[str, Any], ExecutionResult]:
        if variable_values and self.org:
            variable_values["org_id"] = self.org.uid
        return self.client.execute(request, variable_values=variable_values)
    
    def create_org(self, name: str, reverse_id: str) -> str:
        result = self.client.execute(client.create_org, variable_values={"name": name, "reverse_id": reverse_id})
        if "details" in result["orgs"]["create"]:
            return result["orgs"]["create"]["details"]["uid"]
        return None
    
    def invite_to_org(self, reverse_id: str, members: str) -> list[str]:
        result = self.client.execute(client.invite_to_org, variable_values={"reverse_id": reverse_id, "members": members})
        return [r["detail"] for r in result["org"]["addUserByEmail"]]

    def auth(self, username: str, password: str):
        fields = {"username": username, "password": password}
        response = requests.post(self.space_setup.auth_url(), fields)
        return response.json()["access_token"]

    def init_graphql(self) -> tuple[Client, Client]:
        headers = {"Authorization": "Bearer " + self.token}

        transport = RequestsHTTPTransport(url=self.space_setup.graphql_url(), headers=headers)

        ws_url = self.space_setup.ws_url()
        ws_transport = Client(
            transport=WebsocketsTransport(url=ws_url),
            # fetch_schema_from_transport=True,
            execute_timeout=60
        ) if ws_url else None

        return Client(
            transport=transport, fetch_schema_from_transport=True, execute_timeout=600
        ), ws_transport

    def get_org(self, *args, **kwargs) -> schema.LoadedOrgSchema | None:
        result = self.client.execute(client.get_org, variable_values=kwargs)
        if result["org"]:
            org = result["org"]["details"]
            # TODO what is name and slug here, and what is the proper type for schema?
            return schema.LoadedOrgSchema(
                uid=org["uid"],
                # name=org["name"],
                # slug=org["reverseId"],
            )
        return None
    
    def add_secret(self, key: str, value: str, org_id: str | None = None, env_name: str = "default") -> str | None:
        result = None
        if org_id:
            raise NotImplementedError
        else:
            result = self.client.execute(client.add_user_env_secret, variable_values={
                "env_name": env_name,
                "key": key,
                "value": value
            })
            return result["user"]["me"]["env"]["addSecret"]["details"]["uid"]
        return None
    
    def get_secret(self, key: str, org_id: str | None = None, env_name: str = "default") -> str:
        result = None
        if org_id:
            raise NotImplementedError
        else:
            result = self.client.execute(client.get_user_env_secret, variable_values={
                "env_name": env_name,
                "key": key
            })
            return result["user"]["me"]["env"]["key"]["details"]["value"]
        return None

    def _parse_raw_sa(self, raw: dict[str, Any]) -> schema.LoadedSASchema:
        return schema.LoadedSASchema(
            uid=raw["details"]["uid"],
            alias=raw["details"]["alias"],
            core_username=raw["details"]["coreUsername"],
            core_password=raw["details"]["corePassword"],
        )

    def _parse_raw_host(self, raw: dict[str, Any]) -> schema.LoadedHostSchema:
        return schema.LoadedHostSchema(
            uid=raw["details"]["uid"],
            alias=raw["details"]["alias"],
            conn_url=raw["details"]["connUrl"],
            sa=[self._parse_raw_sa(sa["node"]) for sa in raw["mySaOnHost"]["edges"]],
        )

    def create_host(self, *args, **kwargs) -> schema.LoadedHostSchema:
        result = self.client.execute(client.host_create, variable_values=kwargs)
        return self._parse_raw_host(result)

    def get_my_hosts(self, *args, **kwargs) -> list[schema.LoadedHostSchema]:
        result = self.client.execute(client.get_host, variable_values=kwargs)
        return [
            self._parse_raw_host(host["node"])
            for host in result["user"]["me"]["hosts"]["edges"]
        ]

    def create_use_case(self, *args, **kwargs) -> str:
        result = self.client.execute(client.create_use_case, variable_values=kwargs)
        return result["useCases"]["create"]["details"]["uid"]

    def attach_use_case(self, *args, **kwargs) -> bool:
        result = self.client.execute(client.attach_use_case, variable_values=kwargs)
        return result["component"]["attachUseCase"] is not None

    def create_component(self, *args, **kwargs) -> str:
        result = self.client.execute(client.create_component, variable_values=kwargs)
        return result["components"]["create"]["details"]["uid"]
    
    def update_component(self, *args, **kwargs) -> str:
        result = self.client.execute(client.update_component, variable_values=kwargs)
        return result["component"]["update"]["uid"]

    def get_flow_by_version_id(self, *args, **kwargs) -> str | None:
        result = self.client.execute(client.get_flow_by_version_id, variable_values=kwargs)
        return result["version"]["flow"]["details"]["uid"]

    def create_branch(self, *args, **kwargs) -> str:
        result = self.client.execute(client.create_branch, variable_values=kwargs)
        return result["component"]["createBranch"]["details"]["uid"]

    def create_version(self, *args, **kwargs) -> str:
        result = self.client.execute(client.create_version, variable_values=kwargs)
        return result["branch"]["createVersion"]["uid"]

    def create_tag(self, *args, **kwargs) -> str:
        result = self.client.execute(client.create_tag, variable_values=kwargs)
        return result["tags"]["create"]["details"]["uid"]

    def attach_tag_to_comp(self, *args, **kwargs) -> str:
        result = self.client.execute(client.tag_to_comp, variable_values=kwargs)
        return result["component"]["addTag"]

    def create_app_in_version(self, *args, **kwargs) -> str:
        result = self.client.execute(client.app_comp, variable_values=kwargs)
        return result["version"]["addUnderlyingApp"]["uid"]

    def create_flow_in_version(self, *args, **kwargs) -> str:
        result = self.client.execute(client.flow_comp, variable_values=kwargs)
        return result["version"]["addUnderlyingFlow"]["uid"]

    def create_collection(self, *args, **kwargs) -> str:
        result = self._org_request(client.create_collection_alias, variable_values=kwargs)
        return result["collectionAliases"]["create"]["details"]["uid"]

    def create_collection_in_version(self, *args, **kwargs) -> str:
        result = self.client.execute(client.ca_comp, variable_values=kwargs)
        return result["version"]["addUnderlyingCa"]["uid"]

    def get_branch_by_name(self, *args, **kwargs) -> schema.LoadedBranchSchema | None:
        result = self.client.execute(client.branch_by_name, variable_values=kwargs)
        if result["component"]["branches"]["edges"]:
            branch = result["component"]["branches"]["edges"][0]["node"]
            active_version = None
            if branch["activeVersion"] is not None:
                active_version = schema.LoadedVersionSchema(
                    uid=branch["activeVersion"]["details"]["uid"],
                    readable_name=branch["activeVersion"]["details"]["readableName"],
                    updates_markdown=None,
                )
            out = schema.LoadedBranchSchema(
                uid=branch["details"]["uid"],
                name=branch["details"]["name"],
                active_version=active_version,
            )
            return out
        return None

    def add_comp_in_flow(self, *args, **kwargs):
        result = self.client.execute(client.add_comp_to_flow, variable_values=kwargs)
        return result["flow"]["addComponent"]["details"]["uid"]

    def add_app_to_comp_flow(self, *args, **kwargs) -> str:
        result = self.client.execute(client.set_app_in_flow, variable_values=kwargs)
        return result["flow"]["inFlowComponent"]["updateApp"]["details"]["uid"]

    def add_ca_to_comp_flow(self, *args, **kwargs) -> str:
        result = self.client.execute(client.set_ca_in_flow, variable_values=kwargs)
        return result["flow"]["inFlowComponent"]["updateCollectionAlias"]["details"][
            "uid"
        ]

    def link(self, *args, **kwargs) -> str | None:
        result = self.client.execute(client.link_components, variable_values=kwargs)
        if result["flow"]["linkComponents"]["schemaAdapter"] is not None:
            return result["flow"]["linkComponents"]["schemaAdapter"]["details"]["uid"]
        return None

    def add_schema_alias(self, *args, **kwargs) -> str:
        result = self.client.execute(client.add_schema_alias, variable_values=kwargs)
        return result["flow"]["addSchemaAlias"]

    def create_cfg_standalone(self, *args, **kwargs) -> str:
        result = self.client.execute(client.create_cfg, variable_values=kwargs)
        return result["configs"]["update"]["uid"]

    def create_scheme(self, *args, **kwargs) -> str:
        result = self.client.execute(client.create_scheme, variable_values=kwargs)
        return result["schemas"]["create"]["details"]["uid"]

    def create_op(self, *args, **kwargs) -> str:
        result = self.client.execute(client.create_op, variable_values=kwargs)
        return result["ops"]["create"]["details"]["uid"]

    def add_op_2_av(self, *args, **kwargs) -> str:
        result = self.client.execute(client.add_op_to_av, variable_values=kwargs)
        return result["app"]["addOp2Av"]["details"]["uid"]

    def select_active_op(self, *args, **kwargs) -> str:
        result = self.client.execute(client.select_op, variable_values=kwargs)
        return result["flow"]["inFlowComponent"]["selectOp"]["details"]["uid"]

    def set_in_flow_component_cfg(self, *args, **kwargs):
        result = self.client.execute(client.set_in_flow_comp_cfg, variable_values=kwargs)
        return result["flow"]["inFlowComponent"]["updateConfig"]["details"]["uid"]

    def get_schema(self, *args, **kwargs) -> schema.LoadedSchemaSchema | None:
        result = self.client.execute(client.get_schema, variable_values=kwargs)
        if result["schema"]:
            raw = result["schema"]["details"]
            raw["core_id"] = raw["coreId"]
            return schema.LoadedSchemaSchema(**raw)
        return None

    def add_cfg_2_av(self, *args, **kwargs):
        result = self.client.execute(client.add_cfg_2_av, variable_values=kwargs)
        return result["app"]["addCfg2Av"]["details"]["uid"]

    def add_dep_2_op(self, *args, **kwargs):
        result = self.client.execute(client.add_dep_to_op, variable_values=kwargs)
        return result["op"]["addDep"]["details"]["uid"]

    def get_component_by_reverse_id(self, *args, **kwargs) -> dict[str, Any]:
        if not self:
            raise RuntimeError("self is None in get_component_by_reverse_id")
        result = self.client.execute(client.get_comp_with_reverse_id, variable_values=kwargs)
        return result["component"]

    def _parse_loaded_deps(
        self, raw_deps: list[dict[str, Any]]
    ) -> list[schema.LoadedDepSchema]:
        return [
            schema.LoadedDepSchema(
                uid=dep["details"]["uid"],
                key=dep["details"]["key"],
                type=dep["details"]["type"],
            )
            for dep in raw_deps
        ]

    def _parse_loaded_ops(self, raw_ops: list[dict[str, Any]]) -> list[schema.LoadedOpSchema]:
        out = []
        for op in raw_ops:
            op_node = op["node"]
            op_rel = op["rel"]

            def _parse_schema(key):
                loaded_schema = op_node.get(key)
                if loaded_schema:
                    return loaded_schema
                return []

            input_schema = _parse_schema("inputSchema")
            output_schema = _parse_schema("outputSchema")

            details = op_node["details"]

            out.append(
                schema.LoadedOpSchema(
                    uid=op_node["details"]["uid"],
                    core_id=details["coreId"],
                    name=details["name"],
                    doc=details["doc"],
                    finish_msg=details["finishMsg"],
                    tl=details["tl"],
                    query=details["query"],
                    mode=details["mode"],
                    collections_names=details["collectionsNames"],
                    extra_collections_names=details["extraCollectionsNames"],
                    collection_out_names=details["collectionOutNames"],
                    type=op_rel["type"],
                    args=[
                        schema.OpArg(arg_name=arg["argName"], arg_type=arg["argType"], arg_order=arg["argOrder"])
                        for arg in details["args"]
                    ] if details["args"] else None,
                    input_schema=[
                        schema.LoadedSchemaSchema(
                            uid=s["details"]["uid"],
                            core_id=s["details"]["coreId"]
                        )
                        for s in input_schema
                    ],
                    output_schema=[
                        schema.LoadedSchemaSchema(
                            uid=s["details"]["uid"],
                            core_id=s["details"]["coreId"]
                        )
                        for s in output_schema
                    ],
                    requires=self._parse_loaded_deps(op_node.get("deps", [])),
                )
            )
        return out

    def _parse_in_flow_app(self, app_data) -> schema.LoadedInFlowAppSchema | None:
        if app_data:
            return schema.LoadedInFlowAppSchema(
                app_id=app_data["details"]["uid"],
                active_op=[
                    LoadedOpSchema(**y['node']['details'])
                    for y in app_data['op']['edges']
                ]
            )
        return None

    def _parse_in_flow_prompt(self, prompt_data) -> schema.LoadedPromptSchema | None:
        if prompt_data:
            return schema.LoadedPromptSchema(**prompt_data["details"])
        return None

    def _parse_in_flow_component(
        self, in_flow_data: dict[str, Any]
    ) -> schema.LoadedInFlowComponentSchema:
        def _safe(obj, *args):  # noqa: ANN202
            _o = {**obj}
            try:
                for _a in args:
                    _o = _o[_a]
            except:  # noqa: E722
                return None
            return _o

        base_data = {
            "uid": _safe(in_flow_data, "node", "details", "uid"),
            "alias": _safe(in_flow_data, "node", "details", "alias"),
            "app": (
                self._parse_in_flow_app(in_flow_data["node"]["app"])
                if "app" in in_flow_data["node"]
                else None
            ),
            "prompt": (
                self._parse_in_flow_prompt(in_flow_data["node"]["prompt"])
                if "prompt" in in_flow_data["node"]
                else None
            )
        }
        if (
            "component" in in_flow_data["node"]
            and in_flow_data["node"]["component"] is not None
        ):
            base_data["reverse_id"] = in_flow_data["node"]["component"]["details"]["reverseId"]
            base_data["comp_id"] = in_flow_data["node"]["component"]["details"]["uid"]

        if "prev" in in_flow_data["node"]:
            base_data["prev"] = [
                self._parse_in_flow_component(prev)
                for prev in in_flow_data["node"]["prev"]["edges"]
            ]
        try:
            base_data['collection'] = LoadedInFlowCollectionSchema(
                collection_id=in_flow_data['node']['collectionAlias']['details']['uid']
            )
        except (KeyError, ValueError, TypeError):
            pass
        if "cfg" in in_flow_data["node"] and in_flow_data["node"]["cfg"] is not None:
            details = in_flow_data["node"]["cfg"]["details"]
            cfg = schema.LoadedCfgSchema(
                uid=details["uid"],
                readable_name=details["readableName"],
                core_name=details["coreName"],
                core_id=details["coreId"],
                cfg_json=json.loads(details["cfgJson"]) if details["cfgJson"] else None
            )
            base_data["active_cfg"] = cfg
        return schema.LoadedInFlowComponentSchema(**base_data)

    def _parse_comp(self, comp: dict[str, Any]) -> schema.LoadedComponentSchema:
        version = comp["activeBranchVersion"]
        parsed_version = None
        if version:
            details: dict[str, Any] = version["details"]
            version_base_data = {
                "uid": details["uid"],
                "readable_name": details["readableName"],
                "updates_markdown": details["updatesMarkdown"],
            }
            parsed_version = schema.LoadedVersionSchema(**version_base_data)
        details = comp["details"]
        base_data = {
            "uid": details["uid"],
            "name": details["name"],
            "reverse_id": details["reverseId"],
            "branch": schema.LoadedBranchSchema(**comp["activeBranch"]["details"]),
            "version": parsed_version,
            "description": details["descriptionMarkdown"],
        }
        if version and "app" in version and version["app"]:
            base_data["app"] = schema.LoadedAppSchema(
                uid=version["app"]["details"]["uid"],
                container_ref=version["app"]["details"]["containerRef"],
                container_user=version["app"]["details"]["containerUser"],
                container_token=version["app"]["details"]["containerToken"],
                ops=self._parse_loaded_ops(version["app"]["avOp"]["edges"]),
            )
        if version and "flow" in version and version["flow"]:
            base_data["flow"] = schema.LoadedFlowSchema(
                uid=version["flow"]["details"]["uid"],
                components=[
                    self._parse_in_flow_component(in_flow_data)
                    for in_flow_data in version["flow"]["inFlowComponents"]["edges"]
                ],
            )
        if version and "collection" in version and version["collection"]:
            base_data["collection"] = schema.LoadedCollectionAliasSchema(
                uid=version["collection"]["details"]["uid"]
            )
        if version and "asset" in version and version["asset"]:
            base_data["asset"] = schema.Asset(
                uid=version["asset"]["details"]["uid"],
                core_path=version["asset"]["details"]["corePath"],
                download_url=version["asset"]["downloadUrl"],
                upload_url=version["asset"]["uploadUrl"],
            )
        comp = schema.LoadedComponentSchema(**base_data)
        return comp

    def get_parsed_component_by_reverse_id(
        self, *args, **kwargs
    ) -> schema.LoadedComponentSchema | None:
        comp = self.get_component_by_reverse_id(*args, **kwargs)
        if not comp:
            return None
        comp = self._parse_comp(comp)
        return comp

    def get_flow(self, uid: str) -> schema.LoadedFlowSchema:
        results = self.client.execute(client.get_flow, variable_values={"flow_id": uid})
        return schema.LoadedFlowSchema(
            uid=results["flow"]["details"]["uid"],
            components=[
                self._parse_in_flow_component(in_flow_data)
                for in_flow_data in results["flow"]["inFlowComponents"]["edges"]
            ]
        )

    async def subscribe_to_status(self, run_id: str, timeout: int = 150) -> Iterable[schema.RunCompStatus | str]:
        client_ = Client(
            transport=WebsocketsTransport(url=self.space_setup.ws_url()),
            execute_timeout=timeout
        )

        subscription = client_.subscribe_async(
            client.subscribe_to_status,
            variable_values={"run_id": run_id}
        )

        async for result in subscription:
            for run_status in result["runStatus"]:
                if (
                    'task' in run_status
                    and run_status['task']
                    and 'status' in run_status['task']
                    and run_status['task']['status']
                ):
                    yield run_status['task']['status']

                elif 'app' in run_status:
                    yield schema.RunCompStatus(
                        in_flow_comp_id=run_status["app"]["inFlowCompUid"],
                        in_flow_app_id=run_status["app"]["inFlowAppId"],
                        status=run_status["app"]["status"],
                    )
        try:
            subscription.close()
        except (Exception, KeyboardInterrupt):
            pass


    def get_run_status(self, run_id: str) -> tuple[str, list[schema.RunCompStatus]]:
        result = self.client.execute(
            client.get_run_status,
            variable_values={"run_id": run_id}
        )['run']
        run_status = result['details']['state']
        component_statuses = []
        for in_flow_status in result['state']['edges']:
            component_statuses.append(
                schema.RunCompStatus(
                    in_flow_comp_id=in_flow_status['node']['uid'],
                    in_flow_comp_alias=in_flow_status['node']['alias'],
                    status=in_flow_status['rel']['status']
                )
            )
        return run_status, component_statuses

    def _recursively_extract_flow(self, flow_id) -> list[tuple[str, str]]:
        fl = self.get_flow(flow_id)
        components = []
        for comp in fl.components:
            if comp.flow is not None:
                components.extend(self._recursively_extract_flow(comp.flow))
            else:
                components.append((comp.uid, comp.alias,))
        return components

    @overload
    def get_snapshot_components(self, /, task_id: str) -> dict[str, str]:
        pass

    @overload
    def get_snapshot_components(self, /, run_id: str) -> dict[str, str]:
        pass

    def get_snapshot_components(
        self, *, run_id: str = None, task_id = None
    ) -> dict[str, str]:
        if run_id is not None:
            results = self.client.execute(
                client.get_run_snapshot_components, variable_values={
                'run_id': run_id
            })

            components = results['run']['task']['snapshot']['inFlowComponents']['edges']
            dict_ =  {
                c['node']['details']['alias']: c['node']['details']['uid']
                for c in components
            }

            return dict_
        elif task_id is not None:
            results = self.client.execute(
                client.get_task_snapshot_component, variable_values={
                'task_id': task_id
            })

            components = results['task']['snapshot']['inFlowComponents']['edges']
            dict_ =  {
                c['node']['details']['alias']: c['node']['details']['uid']
                for c in components
            }

            return dict_
        else:
            raise ValueError("Either task_id or run_id should be passed")


    def malevich(self, prompt: str, max_depth: int = 1) -> tuple[str, str]:
        res = self.client.execute(
            client.add_pt_2_malevich,
            variable_values={"prompt": prompt, "max_depth": max_depth},
        )

        pt_id = res["malevich"]["addPt"]["details"]["uid"]
        thought_id = res["malevich"]["addPt"]["thoughts"]["edges"][0]["node"][
            "details"
        ]["uid"]

        return pt_id, thought_id

    def generate_flow(self, *args, **kwargs) -> schema.LoadedFlowSchema:
        result = self.client.execute(client.generate_workflow, variable_values=kwargs)

        flow_node = result["malevich"]["pt"]["generateFlow"]["edges"][0]["node"]

        return schema.LoadedFlowSchema(
            uid=flow_node["details"]["uid"],
            components=[
                self._parse_in_flow_component(in_flow_data)
                for in_flow_data in flow_node["inFlowComponents"]["edges"]
            ],
        )

    def build_task(self, *args, **kwargs) -> list[str]:
        result = self._org_request(client.build_task, variable_values=kwargs)
        return [
            created["uid"] for created in result["flow"]["buildCoreTask"]
        ]
    
    def build_task_v2(self, *args, **kwargs) -> str | None:
        result = self._org_request(client.build_task_v2, variable_values=kwargs)
        if "uid" in result["flow"]["buildV2"]:
            return result["flow"]["buildV2"]
        return None

    def boot_task(self, *args, **kwargs) -> str:
        result = self.client.execute(client.boot_task, variable_values=kwargs)
        return result["task"]["boot"]["details"]["uid"]

    def change_task_state(self, *args, **kwargs) -> str:
        result = self.client.execute(client.change_task_state, variable_values=kwargs)
        return result["task"]["changeState"]["details"]["uid"]

    def get_ca_in_flow(self, flow_id: str, in_flow_id: str):
        """Gets CA uid of in-flow component

        Args:
            flow_id (str): uid of flow
            in_flow_id (str): uid of collection component within flow

        Returns:
            uid of CA
        """
        result = self.client.execute(client.get_ca_in_flow, variable_values={
            'flow_id': flow_id,
            'in_flow_id': in_flow_id
        })
        return result['flow']['inFlowComponent']['collectionAlias']['collection']['details']['uid']
    
    def update_ca(self, *args, **kwargs) -> str:
        result = self.client.execute(client.update_collection_alias, variable_values=kwargs)
        return result["collectionAlias"]["update"]["uid"]

    def get_task_start_schema(self, task_id: str) -> list[schema.LoadedTaskStartSchema]:
        result = self.client.execute(client.get_task_start_schema, variable_values={"task_id": task_id})
        if "startSchema" not in result["task"]:
            return []
        return [
            schema.LoadedTaskStartSchema(
                **{
                    "in_flow_id": start["inFlowId"],
                    "ca_alias": start["caAlias"],
                    "injected_alias": start["injectedAlias"]
                }
            )
            for start in result["task"]["startSchema"]
        ]

    def run_task(self, *args, **kwargs) -> str:
        result = self._org_request(client.run_task, variable_values=kwargs)
        return result["runWithStatus"]["details"]["uid"]

    def wipe_component(self, uid: Optional[str] = None, reverse_id: Optional[str] = None) -> bool:
        kwargs = {
            "uid": uid,
            "reverse_id": reverse_id
        }
        result = self.client.execute(client.wipe_component, variable_values=kwargs)
        return result["component"]["wipe"]

    def get_api_token_by_name(self, name: str) -> str | None:
        result = self.client.execute(client.api_key_by_name, variable_values={"name": name})
        by_name = result["apiKey"]["byName"]
        if "details" in by_name:
            return by_name["details"]
        return None

    def get_results(self, run_id: str, in_flow_id: str) -> list[schema.ResultSchema]:
        result = self.client.execute(
            client.get_in_flow_results,
            variable_values={"run_id": run_id, "in_flow_id": in_flow_id}
        )
        outputs = []
        for result in result['run']['interCa']['edges']:
            ca_details = result['node']['ca']['details']
            schema_details = result['node']['ca']['schema']
            ca = schema.LoadedCollectionAliasSchema(
                uid=ca_details['uid'],
                core_alias=ca_details['coreAlias'],
                core_id=ca_details['coreId'],
                schema_core_id=None if not schema_details else schema_details['details']['coreId']
            )
            docs = [json.loads(x['node']['rawJson']) for x in result['node']['ca']['coreTable']['edges']]

            outputs.append(schema.ResultSchema(
                ca=ca,
                raw_json=docs
            ))

        return outputs

    def create_endpoint(self, task_id: str, alias: str | None, token: str | None) -> tuple[str, str]:
        kwargs = {
            "task_id": task_id,
            "alias": alias,
            "api_key": []
        }
        if token:
            token_id = self.get_api_token_by_name(name=token)
            kwargs["api_key"] = [token_id]
        result = self.client.execute(client.create_task_endpoint, variable_values=kwargs)
        endpoint_uid = result["task"]["createEndpoint"]["details"]["uid"]
        core_url = result["task"]["createEndpoint"]["invokationUrl"]
        return endpoint_uid, core_url
    
    def update_endpoint(self, endpoint_id: str, new_task_id: str):
        result = self.client.execute(client.update_endpoint_in_task, variable_values={
            "endpoint_id": endpoint_id,
            "task_id": new_task_id
        })
    
    def invoke(self, component: str, payload: schema.InvokePayload, branch: str | None = None) -> tuple[str, str] | None:
        kwargs = {
            "component": component,
            "branch": branch,
            "payload": [p.model_dump() for p in payload.payload],
            "webhook": payload.webhook
        }
        result = self._org_request(client.invoke_component, variable_values=kwargs)
        if result["invoke"] is None:
            return None
        task = result["invoke"]["task"]
        run = result["invoke"]["run"]
        return task["details"]["uid"], run["details"]["uid"]
    
    def add_comp_to_org(self, *, comp_id: str, org_id: str) -> str | None:
        kwargs = {
            "comp_id": comp_id,
            "org_id": org_id
        }
        result = self.client.execute(client.comp_to_org, variable_values=kwargs)
        if "details" not in result["component"]["addToOrg"]:
            return None
        return result["component"]["addToOrg"]["details"]["uid"]
    
    def create_asset(
            self,
            *,
            asset: schema.CreateAsset,
            host_id: str | None = None
    ) -> schema.Asset:
        kwargs = asset.model_dump()
        kwargs["host_id"] = host_id
        result = self._org_request(client.create_asset, variable_values=kwargs)
        return self._parse_asset(result["assets"]["create"])
    
    def _parse_asset(self, asset: dict[str, Any]) -> schema.Asset:
        raw = asset["details"]
        raw["core_path"] = raw["corePath"]
        raw["is_composite"] = raw["isComposite"]
        if "downloadUrl" in asset:
            raw["download_url"] = asset["downloadUrl"]
        if "uploadUrl" in asset:
            raw["upload_url"] = asset["uploadUrl"]
        return schema.Asset.model_validate(raw)
    
    def get_asset(self, *, uid: str) -> schema.Asset:
        result = self.client.execute(client.get_asset, variable_values={"uid": uid})
        return self._parse_asset(result["asset"])
    
    def create_asset_in_version(
            self, *, version_id: str, asset: schema.CreateAsset, host_id: str | None = None
    ) -> schema.Asset:
        kwargs = asset.model_dump()
        kwargs["version_id"] = version_id
        kwargs["host_id"] = host_id
        result = self._org_request(client.create_asset_in_version, variable_values=kwargs)
        return self._parse_asset(result["version"]["createUnderlyingAsset"])

    def auto_layout(self, *, flow: str):
        self.client.execute(client.auto_layout, variable_values={"flow": flow})

    def get_task_core_id(self, *, task_id: str) -> tuple[str, str]:
        result = self._org_request(client.get_task_core_id, variable_values={"task_id": task_id})
        return result["task"]["details"]["coreId"], result["task"]["component"]["details"]["reverseId"]
    
    def get_deployments_by_reverse_id(self, *, reverse_id: str, status: list[str] | None = None) -> list[schema.LoadedTaskSchema]:
        results = self._org_request(client.get_deployments_for_reverse_id, variable_values={"reverse_id": reverse_id, "status": status})
        results = results["tasks"]["component"]["edges"]

        out = []

        for result in results:
            task = result["node"]
            details = task["details"]
            out.append(
                schema.LoadedTaskSchema(
                    uid=details["uid"],
                    state=details["bootState"],
                    core_id=details["coreId"],
                    last_runned_at=details["lastRunnedAt"]
                )
            )

        return out
