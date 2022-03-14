import pytest

from opera_tosca_parser.error import ParseError
from opera_tosca_parser.parser.tosca.v_1_3.import_definition import ImportDefinition
from opera_tosca_parser.parser.yaml.node import Node


class TestNormalizeDefinition:
    def test_noop_for_dicts(self):
        node = Node({})
        assert ImportDefinition.normalize(node) == node

    def test_string_normalization(self):
        assert ImportDefinition.normalize(Node("a")).bare == {"file": "a"}

    @pytest.mark.parametrize("data", [123, 1.4, []])
    def test_failed_normalization(self, data):
        with pytest.raises(ParseError, match="string or dict"):
            ImportDefinition.normalize(Node(data))


class TestParse:
    def test_full(self, yaml_ast):
        ImportDefinition.parse(yaml_ast(
            # language=yaml
            """
            file: my/file
            repository: my_repo
            namespace_prefix: prefix
            namespace_uri: some_uri
            """
        ))

    def test_minimal(self, yaml_ast):
        ImportDefinition.parse(yaml_ast(
            # language=yaml
            """
            file: my/file
            """
        ))
