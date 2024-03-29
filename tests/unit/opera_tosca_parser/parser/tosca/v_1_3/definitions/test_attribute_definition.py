from opera_tosca_parser.parser.tosca.v_1_3.definitions.attribute_definition import AttributeDefinition


class TestParse:
    def test_full(self, yaml_ast):
        AttributeDefinition.parse(yaml_ast(
            # language=yaml
            """
            type: my_type
            description: Some desc
            default: 5
            status: deprecated
            key_schema:
              type: integer
            entry_schema:
              type: integer
            """
        ))

    def test_minimal(self, yaml_ast):
        AttributeDefinition.parse(yaml_ast("type: my_type"))
