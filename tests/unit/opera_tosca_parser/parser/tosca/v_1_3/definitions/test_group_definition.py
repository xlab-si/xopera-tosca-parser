from opera_tosca_parser.parser.tosca.v_1_3.definitions.group_definition import GroupDefinition


class TestParse:
    def test_full(self, yaml_ast):
        GroupDefinition.parse(yaml_ast(
            # language=yaml
            """
            type: node.type
            description: Text
            metadata: {}
            properties: {}
            members:
              - node_template_1
              - node_template_2
              - node_template_3
            """
        ))

    def test_minimal(self, yaml_ast):
        GroupDefinition.parse(yaml_ast(
            # language=yaml
            """
            type: group.type
            """
        ))
