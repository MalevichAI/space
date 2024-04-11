from malevich_space.schema import ComponentSchema, Asset, VersionMode
from malevich_space.ops.roller import local_roller
from malevich_space.ops import SlowComponentManager


test_asset_schema = ComponentSchema(
    name="test_asset",
    reverse_id="__internal_test_asset",
    description="Test asset for internal testing",
    asset=Asset(
        core_path="__internal_test_core_path"
    )
)


def test_upload_asset():
    roller = local_roller(None, None, comp_manager_generator=SlowComponentManager)
    roller.component(test_asset_schema, version_mode=VersionMode.MINOR)

    loaded = roller.comp_manager.space.get_parsed_component_by_reverse_id(reverse_id=test_asset_schema.reverse_id)
    
    assert loaded and loaded.asset
