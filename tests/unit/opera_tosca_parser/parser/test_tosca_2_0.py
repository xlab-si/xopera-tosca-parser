import pathlib

import pytest

from opera_tosca_parser.error import ParseError
from opera_tosca_parser.parser import tosca


class TestLoad:
    def test_load_minimal_document(self, tmp_path):
        name = pathlib.PurePath("root.yaml")
        (tmp_path / name).write_text("tosca_definitions_version: tosca_2_0")

        doc = tosca.load_service_template(tmp_path, name)
        assert doc.tosca_definitions_version.data == "tosca_2_0"

    def test_empty_document_is_invalid(self, tmp_path):
        name = pathlib.PurePath("empty.yaml")
        (tmp_path / name).write_text("{}")
        with pytest.raises(ParseError):
            tosca.load_service_template(tmp_path, name)

    @pytest.mark.parametrize("typ", [
        ("data_types", "xml"),
        ("artifact_types", "Root"),
        ("capability_types", "Node"),
        ("relationship_types", "HostedOn"),
        ("interface_types", "Lifecycle.Standard"),
        ("node_types", "Root"),
        ("group_types", "Root"),
        ("policy_types", "Scaling")
    ])
    def test_stdlib_is_present(self, tmp_path, typ):
        name = pathlib.PurePath("stdlib.yaml")
        (tmp_path / name).write_text(
            # language=yaml
            f"""
            tosca_definitions_version: tosca_2_0
            imports:
              - profile: org.oasis-open.tosca.simple:2.0
            """
        )

        doc = tosca.load_service_template(tmp_path, name)
        assert doc.dig(*typ) is not None

    @pytest.mark.parametrize("typ", [
        ("data_types", "xml"),
        ("artifact_types", "Root"),
        ("capability_types", "Node"),
        ("relationship_types", "HostedOn"),
        ("interface_types", "Lifecycle.Standard"),
        ("node_types", "Root"),
        ("group_types", "Root"),
        ("policy_types", "Scaling")
    ])
    def test_custom_type_is_present(self, tmp_path, yaml_text, typ):
        name = pathlib.PurePath("custom.yaml")
        (tmp_path / name).write_text(yaml_text(
            # language=yaml
            f"""
            tosca_definitions_version: tosca_2_0
            imports:
              - profile: org.oasis-open.tosca.simple:2.0
            {typ[0]}:
              my.custom.Type:
                derived_from: {typ[1]}
            """
        ))

        doc = tosca.load_service_template(tmp_path, name)
        assert doc.dig(typ[0], "my.custom.Type") is not None

    def test_loads_template_part(self, tmp_path, yaml_text):
        name = pathlib.PurePath("template.yaml")
        (tmp_path / name).write_text(yaml_text(
            # language=yaml
            """
            tosca_definitions_version: tosca_2_0
            imports:
              - profile: org.oasis-open.tosca.simple:2.0
            topology_template:
              node_templates:
                my_node:
                  type: SoftwareComponent
            """
        ))

        doc = tosca.load_service_template(tmp_path, name)
        assert doc.topology_template.node_templates["my_node"] is not None

    def test_load_from_csar_subfolder(self, tmp_path, yaml_text):
        name = pathlib.PurePath("sub/folder/file.yaml")
        (tmp_path / name).parent.mkdir(parents=True)
        (tmp_path / name).write_text(yaml_text(
            # language=yaml
            """
            tosca_definitions_version: tosca_2_0
            imports:
              - imp.yaml
            """
        ))
        (tmp_path / "sub/folder/imp.yaml").write_text(yaml_text(
            # language=yaml
            """
            tosca_definitions_version: tosca_2_0
            imports:
              - profile: org.oasis-open.tosca.simple:2.0
            data_types:
              my_type:
                derived_from: xml
            """
        ))

        doc = tosca.load_service_template(tmp_path, name)
        assert doc.data_types["my_type"]

    def test_duplicate_import(self, tmp_path, yaml_text):
        name = pathlib.PurePath("template.yaml")
        (tmp_path / name).write_text(yaml_text(
            # language=yaml
            """
            tosca_definitions_version: tosca_2_0
            imports: [ template.yaml ]
            """
        ))
        tosca.load_service_template(tmp_path, name)

    def test_imports_from_multiple_levels(self, tmp_path, yaml_text):
        name = pathlib.PurePath("template.yaml")
        (tmp_path / name).write_text(yaml_text(
            # language=yaml
            """
            tosca_definitions_version: tosca_2_0
            imports:
              - subfolder/a.yaml
              - subfolder/b.yaml
            """
        ))
        (tmp_path / "subfolder").mkdir()
        (tmp_path / "subfolder/a.yaml").write_text(yaml_text(
            # language=yaml
            """
            tosca_definitions_version: tosca_2_0
            imports:
              - b.yaml
            """
        ))
        (tmp_path / "subfolder/b.yaml").write_text(yaml_text(
            # language=yaml
            """
            tosca_definitions_version: tosca_2_0
            imports:
              - profile: org.oasis-open.tosca.simple:2.0
            data_types:
              my_type:
                derived_from: xml
            """
        ))

        tosca.load_service_template(tmp_path, name)

    def test_merge_topology_template(self, tmp_path, yaml_text):
        name = pathlib.PurePath("template.yaml")
        (tmp_path / name).write_text(yaml_text(
            # language=yaml
            """
            tosca_definitions_version: tosca_2_0
            imports:
              - profile: org.oasis-open.tosca.simple:2.0
              - merge.yaml
            topology_template:
              inputs:
                some-input:
                  type: string
              node_templates:
                my_node:
                  type: SoftwareComponent
            """
        ))
        (tmp_path / "merge.yaml").write_text(yaml_text(
            # language=yaml
            """
            tosca_definitions_version: tosca_2_0
            topology_template:
              inputs:
                other-input:
                  type: string
              node_templates:
                other_node:
                  type: SoftwareComponent
            """
        ))
        tosca.load_service_template(tmp_path, name)

    def test_merge_duplicate_node_templates_invalid(self, tmp_path, yaml_text):
        name = pathlib.PurePath("template.yaml")
        (tmp_path / name).write_text(yaml_text(
            # language=yaml
            """
            tosca_definitions_version: tosca_2_0
            imports:
              - merge1.yaml
              - merge2.yaml
            topology_template:
              node_templates:
                my_node:
                  type: SoftwareComponent
            """
        ))
        (tmp_path / "merge1.yaml").write_text(yaml_text(
            # language=yaml
            """
            tosca_definitions_version: tosca_2_0
            topology_template:
              node_templates:
                other_node:
                  type: SoftwareComponent
            """
        ))
        (tmp_path / "merge2.yaml").write_text(yaml_text(
            # language=yaml
            """
            tosca_definitions_version: tosca_2_0
            topology_template:
              node_templates:
                other_node:
                  type: SoftwareComponent
            """
        ))
        with pytest.raises(ParseError):
            tosca.load_service_template(tmp_path, name)


class TestExecute:
    def test_undefined_required_properties1(self, tmp_path, yaml_text):
        name = pathlib.PurePath("template.yaml")
        (tmp_path / name).write_text(yaml_text(
            # language=yaml
            """
            tosca_definitions_version: tosca_2_0
            imports:
              - profile: org.oasis-open.tosca.simple:2.0
            node_types:
              my_node_type:
                derived_from: Root
                attributes:
                  test_attribute:
                    type: boolean
                properties:
                  test_property1:
                    type: integer
                    required: false
                  test_property2:
                    type: float
                    default: 42.0
                    required: true
                  test_property3:
                    type: string
                    required: true
            topology_template:
              node_templates:
                my_node_template:
                  type: my_node_type
            """
        ))
        ast = tosca.load_service_template(tmp_path, name)
        with pytest.raises(ParseError, match="Missing a required property: test_property3"):
            ast.get_template({})

    def test_undefined_required_properties2(self, tmp_path, yaml_text):
        name = pathlib.PurePath("template.yaml")
        (tmp_path / name).write_text(yaml_text(
            # language=yaml
            """
            tosca_definitions_version: tosca_2_0
            imports:
              - profile: org.oasis-open.tosca.simple:2.0
            node_types:
              my_node_type:
                derived_from: Root
                properties:
                  test_prop1:
                    type: integer
                    required: false
                  test_prop2:
                    type: float
                    default: 42.0
                  test_prop3:
                    type: string
            topology_template:
              node_templates:
                my_node_template:
                  type: my_node_type
            """
        ))
        ast = tosca.load_service_template(tmp_path, name)
        with pytest.raises(ParseError, match="Missing a required property: test_prop3"):
            ast.get_template({})

    def test_undefined_required_properties3(self, tmp_path, yaml_text):
        name = pathlib.PurePath("template.yaml")
        (tmp_path / name).write_text(yaml_text(
            # language=yaml
            """
            tosca_definitions_version: tosca_2_0
            imports:
              - profile: org.oasis-open.tosca.simple:2.0
            node_types:
              my_node_type:
                derived_from: Root
                properties:
                  property1:
                    type: integer
                  property2:
                    type: float
                  property3:
                    type: string
            topology_template:
              node_templates:
                my_node_template:
                  type: my_node_type
                  properties:
                    property1: 42
                    property2: 42.0
            """
        ))
        ast = tosca.load_service_template(tmp_path, name)
        with pytest.raises(ParseError, match="Missing a required property: property3"):
            ast.get_template({})

    def test_undeclared_requirements(self, tmp_path, yaml_text):
        name = pathlib.PurePath("template.yaml")
        (tmp_path / name).write_text(yaml_text(
            # language=yaml
            """
            tosca_definitions_version: tosca_2_0
            imports:
              - profile: org.oasis-open.tosca.simple:2.0
            topology_template:
              node_templates:
                node_1:
                  type: Root
                node_2:
                  type: Root
                  requirements:
                    - dependency: node_1
                node_3:
                  type: Root
                  requirements:
                    - dependency_not_defined1: node_2
        """
        ))
        ast = tosca.load_service_template(tmp_path, name)
        with pytest.raises(ParseError, match="Undeclared requirements: dependency_not_defined1"):
            ast.get_template({})
