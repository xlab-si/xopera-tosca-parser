from opera_tosca_parser.parser.tosca.v_2_0.definitions.node_filter_definition import NodeFilterDefinition


class TestParse:
    def test_full(self, yaml_ast):
        NodeFilterDefinition.parse(yaml_ast(
            # language=yaml
            """
            properties:
              - num_cpus: { in_range: [ 3, 6 ] }
            capabilities: []
            """
        ))

    def test_minimal(self, yaml_ast):
        NodeFilterDefinition.parse(yaml_ast("{}"))
