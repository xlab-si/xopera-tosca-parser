from opera_tosca_parser.parser.tosca.v_2_0.definitions.node_template import NodeTemplate


class TestParse:
    def test_full(self, yaml_ast):
        NodeTemplate.parse(yaml_ast(
            # language=yaml
            """
            type: node.type
            description: Text
            metadata: {}
            directives: []
            properties: {}
            attributes: {}
            requirements: []
            capabilities: {}
            interfaces: {}
            artifacts: {}
            node_filter: {}
            copy: template_name
            """
        ))

    def test_minimal(self, yaml_ast):
        NodeTemplate.parse(yaml_ast(
            # language=yaml
            """
            type: node.type
            """
        ))
