from opera_tosca_parser.parser.tosca.v_2_0.definitions.parameter_definition import ParameterDefinition


class TestParse:
    def test_full(self, yaml_ast):
        ParameterDefinition.parse(yaml_ast(
            # language=yaml
            """
            type: data_type_name
            description: My text
            required: true
            default: 567
            status: supported
            constraints: []
            key_schema:
              type: string
            entry_schema:
              type: timestamp
            external_schema: schema
            metadata: {}
            value: 987
            """
        ))

    def test_minimal(self, yaml_ast):
        ParameterDefinition.parse(yaml_ast("{}"))
