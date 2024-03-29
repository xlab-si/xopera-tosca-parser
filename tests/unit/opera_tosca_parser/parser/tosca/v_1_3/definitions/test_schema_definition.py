from opera_tosca_parser.parser.tosca.v_1_3.definitions.schema_definition import SchemaDefinition


class TestParse:
    def test_full(self, yaml_ast):
        SchemaDefinition.parse(yaml_ast(
            # language=yaml
            """
            type: my_type
            description: My description
            constraints: []
            """
        ))

    def test_minimal(self, yaml_ast):
        SchemaDefinition.parse(yaml_ast(
            # language=yaml
            """
            type: my_type
            """
        ))
