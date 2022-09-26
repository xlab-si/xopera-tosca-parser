from opera_tosca_parser.parser.tosca.v_2_0.definitions.event_filter_definition import EventFilterDefinition


class TestParse:
    def test_full(self, yaml_ast):
        EventFilterDefinition.parse(yaml_ast(
            # language=yaml
            """
            node: node_type_name
            requirement: requirement_name
            capability: capability_name
            """
        ))

    def test_minimal(self, yaml_ast):
        EventFilterDefinition.parse(yaml_ast(
            # language=yaml
            """
            node: node_template_name
            """
        ))
