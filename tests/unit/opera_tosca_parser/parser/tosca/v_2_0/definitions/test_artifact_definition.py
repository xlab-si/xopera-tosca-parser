import pytest

from opera_tosca_parser.error import ParseError
from opera_tosca_parser.parser.tosca.v_2_0.definitions.artifact_definition import ArtifactDefinition
from opera_tosca_parser.parser.yaml.node import Node


class TestNormalize:
    @pytest.mark.parametrize("data", [1, 2.3, True, (), []])
    def test_invalid_data(self, data):
        with pytest.raises(ParseError):
            ArtifactDefinition.normalize(Node(data))

    def test_string_normalization(self):
        obj = ArtifactDefinition.normalize(Node("string"))

        assert obj.bare == {
            "type": "File",
            "file": "string",
        }

    def test_dict_normalization(self):
        node = Node({})
        obj = ArtifactDefinition.normalize(node)

        assert obj == node


class TestParse:
    def test_full(self, yaml_ast):
        ArtifactDefinition.parse(yaml_ast(
            # language=yaml
            """
            description: My arty desc
            type: my.type
            file: some/file
            repository: repo reference
            deploy_path: another/path
            checksum: abcsdfkjrkfsdjdbhf
            checksum_algorithm: SHA256
            properties:
              prop: val
            """
        ))

    def test_minimal(self, yaml_ast):
        ArtifactDefinition.parse(yaml_ast(
            # language=yaml
            """
            type: my.type
            file: some/file
            """
        ))
