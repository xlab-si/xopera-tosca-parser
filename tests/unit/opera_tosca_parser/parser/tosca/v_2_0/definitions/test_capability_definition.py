from opera_tosca_parser.parser.tosca.v_2_0.definitions.capability_definition import CapabilityDefinition


class TestParse:
    def test_full(self, yaml_ast):
        CapabilityDefinition.parse(yaml_ast(
            # language=yaml
            """
            type: cap_type_name
            description: Some text
            properties: {}
            attributes: {}
            valid_source_node_types: []
            """
        ))

    def test_minimal(self, yaml_ast):
        CapabilityDefinition.parse(yaml_ast(
            # language=yaml
            """
            type: cap_type_name
            """
        ))
