from opera_tosca_parser.parser.tosca.v_2_0.definitions.relationship_type import RelationshipType


class TestParse:
    def test_full(self, yaml_ast):
        RelationshipType.parse(yaml_ast(
            # language=yaml
            """
            derived_from: relationship_type
            description: My desc
            metadata:
              key: value
            version: "1.2"
            properties: {}
            attributes: {}
            interfaces: {}
            valid_capability_types: [ a, b, c ]
            """
        ))

    def test_minimal(self, yaml_ast):
        RelationshipType.parse(yaml_ast(
            # language=yaml
            """
            derived_from: relationship_type
            """
        ))
