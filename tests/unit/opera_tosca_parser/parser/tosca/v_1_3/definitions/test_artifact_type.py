from opera_tosca_parser.parser.tosca.v_1_3.definitions.artifact_type import ArtifactType


class TestParse:
    def test_full(self, yaml_ast):
        ArtifactType.parse(yaml_ast(
            # language=yaml
            """
            derived_from: artifact_type
            description: My desc
            metadata:
              key: value
            version: "1.2"
            mime_type: applicaton/json
            file_ext: [ json, jsn ]
            properties:
              prop:
                type: prop_type
            """
        ))

    def test_minimal(self, yaml_ast):
        ArtifactType.parse(yaml_ast(
            # language=yaml
            """
            derived_from: artifact_type
            """
        ))
