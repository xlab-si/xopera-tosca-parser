import pytest

from opera_tosca_parser.error import ParseError
from opera_tosca_parser.parser.tosca.v_1_3.definitions.repository_definition import RepositoryDefinition
from opera_tosca_parser.parser.yaml.node import Node


class TestNormalize:
    def test_noop_for_dicts(self):
        node = Node({})
        assert RepositoryDefinition.normalize(node) == node

    def test_string_normalization(self):
        assert RepositoryDefinition.normalize(Node("a")).bare == {"url": "a"}

    @pytest.mark.parametrize("data", [123, 1.4, []])
    def test_failed_normalization(self, data):
        with pytest.raises(ParseError, match="string or dict"):
            RepositoryDefinition.normalize(Node(data))


class TestParse:
    def test_full(self, yaml_ast):
        RepositoryDefinition.parse(yaml_ast(
            # language=yaml
            """
            description: My description
            url: https://repo.name
            credential:
              token: my_pass
            """
        ))

    def test_minimal(self, yaml_ast):
        RepositoryDefinition.parse(yaml_ast(
            # language=yaml
            """
            url: https://repo.name
            """
        ))
