from opera_tosca_parser.parser.tosca.v_1_3.definitions.capability_assignment import CapabilityAssignment


class TestParse:
    def test_full(self, yaml_ast):
        CapabilityAssignment.parse(yaml_ast(
            # language=yaml
            """
            properties:
              prop: value
            attributes:
              attr: value
            occurrences: [ 0, UNBOUNDED ]
            """
        ))

    def test_minimal(self, yaml_ast):
        CapabilityAssignment.parse(yaml_ast("{}"))
