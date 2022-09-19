from opera_tosca_parser.parser.tosca.v_1_3.definitions.interface_definition_for_type import InterfaceDefinitionForType


class TestParse:
    def test_full(self, yaml_ast):
        InterfaceDefinitionForType.parse(yaml_ast(
            # language=yaml
            """
            inputs: {}
            operations: {}
            notifications: {}
            """
        ))

    def test_minimal(self, yaml_ast):
        InterfaceDefinitionForType.parse(yaml_ast("{}"))
