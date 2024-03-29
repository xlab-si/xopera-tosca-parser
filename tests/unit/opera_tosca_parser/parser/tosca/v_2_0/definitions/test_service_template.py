import pytest

from opera_tosca_parser.error import ParseError
from opera_tosca_parser.parser.tosca.v_2_0.definitions.service_template import ServiceTemplate
from opera_tosca_parser.parser.yaml.node import Node


class TestNormalizeDefinition:
    def test_noop_for_dicts_with_no_dsl_definitions(self):
        assert ServiceTemplate.normalize(Node({})).bare == {}

    def test_dsl_definitions_removal(self):
        assert ServiceTemplate.normalize(Node({Node("dsl_definitions"): "data"})).bare == {}

    @pytest.mark.parametrize("data", [123, 1.4, []])
    def test_failure_with_non_dict_data(self, data):
        with pytest.raises(ParseError):
            ServiceTemplate.normalize(Node(data))


class TestParse:
    def test_full(self, yaml_ast, tmp_path):
        ServiceTemplate.parse_service_template(yaml_ast(
            # language=yaml
            """
            tosca_definitions_version: tosca_2_0
            profile: my_profile
            metadata: {}
            description: Text here
            dsl_definitions:
              arbitrary_data: can
              be: here
              since:
                - it
                - is
                - stripped: from
                  the: doc
            repositories: {}
            imports: []
            artifact_types: {}
            data_types: {}
            capability_types: {}
            interface_types: {}
            relationship_types: {}
            node_types: {}
            group_types: {}
            policy_types: {}
            topology_template: {}
            """
        ), tmp_path, tmp_path, set())

    def test_minimal(self, yaml_ast, tmp_path):
        ServiceTemplate.parse_service_template(yaml_ast(
            # language=yaml
            """
            tosca_definitions_version: tosca_2_0
            """
        ), tmp_path, tmp_path, set())


class TestMerge:
    def test_valid_section_merge(self, yaml_ast, tmp_path):
        template = ServiceTemplate.parse_service_template(yaml_ast(
            # language=yaml
            """
            tosca_definitions_version: tosca_2_0
            node_types:
              type_a:
                derived_from: a
            """
        ), tmp_path, tmp_path, set())[0]
        template.merge(ServiceTemplate.parse_service_template(yaml_ast(
            # language=yaml
            """
            tosca_definitions_version: tosca_2_0
            node_types:
              type_b:
                derived_from: b
            """
        ), tmp_path, tmp_path, set())[0])

        assert len(template.node_types.data) == 2
        assert template.node_types["type_a"].data["derived_from"].data == "a"
        assert template.node_types["type_b"].data["derived_from"].data == "b"

    def test_valid_merge(self, yaml_ast, tmp_path):
        template = ServiceTemplate.parse_service_template(yaml_ast(
            """
            tosca_definitions_version: tosca_2_0
            data_types:
              type_a:
                derived_from: a
            """
        ), tmp_path, tmp_path, set())[0]
        template.merge(ServiceTemplate.parse_service_template(yaml_ast(
            # language=yaml
            """
            tosca_definitions_version: tosca_2_0
            node_types:
              type_a:
                derived_from: a
            """
        ), tmp_path, tmp_path, set())[0])

        assert len(template.data_types.data) == 1
        assert template.node_types["type_a"].data["derived_from"].data == "a"

    def test_duplicates(self, yaml_ast, tmp_path):
        with pytest.raises(ParseError, match="type_a"):
            ServiceTemplate.parse_service_template(yaml_ast(
                # language=yaml
                """
                tosca_definitions_version: tosca_2_0
                node_types:
                  type_a:
                    derived_from: a
                """
            ), tmp_path, tmp_path, set())[0].merge(ServiceTemplate.parse_service_template(yaml_ast(
                # language=yaml
                """
                tosca_definitions_version: tosca_2_0
                node_types:
                  type_a:
                    derived_from: b
                """
            ), tmp_path, tmp_path, set())[0])
