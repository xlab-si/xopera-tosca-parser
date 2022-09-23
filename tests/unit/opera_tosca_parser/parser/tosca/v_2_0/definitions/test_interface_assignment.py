from opera_tosca_parser.parser.tosca.v_2_0.definitions.interface_assignment import InterfaceAssignment


class TestParse:
    def test_full(self, yaml_ast):
        InterfaceAssignment.parse(yaml_ast(
            # language=yaml
            """
            inputs:
              in: put
            operations:
              op: artifact
            notifications:
              my_notification:
                implementation:
                    primary: primary_artifact_definition
            """
        ))

    def test_minimal(self, yaml_ast):
        InterfaceAssignment.parse(yaml_ast("{}"))
