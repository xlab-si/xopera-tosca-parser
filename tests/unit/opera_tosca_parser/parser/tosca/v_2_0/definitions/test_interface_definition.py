from opera_tosca_parser.parser.tosca.v_2_0.definitions.interface_definition import InterfaceDefinition


class TestParse:
    def test_full(self, yaml_ast):
        InterfaceDefinition.parse(yaml_ast(
            # language=yaml
            """
            inputs: {}
            operations: {}
            notifications: {}
            """
        ))

    def test_minimal(self, yaml_ast):
        InterfaceDefinition.parse(yaml_ast("{}"))
