from opera_tosca_parser.parser.tosca.v_1_3.definitions.relationship_template import RelationshipTemplate


class TestParse:
    def test_full(self, yaml_ast):
        RelationshipTemplate.parse(yaml_ast(
            # language=yaml
            """
            type: rel.type
            description: Some muttering
            metadata: {}
            properties:
              prop: 4
            attributes:
              attr: 6
            interfaces:
              Standard:
                operations:
                  create: path/to/playbook.yaml
            copy: other_template_name
            """
        ))

    def test_minimal(self, yaml_ast):
        RelationshipTemplate.parse(yaml_ast(
            # language=yaml
            """
            type: rel.type
            """
        ))
