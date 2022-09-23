import pytest

from opera_tosca_parser.error import ParseError
from opera_tosca_parser.parser.tosca.v_1_3.definitions.notification_implementation_definition import \
    NotificationImplementationDefinition
from opera_tosca_parser.parser.yaml.node import Node


class TestNormalize:
    @pytest.mark.parametrize("data", [1, 2.3, True, (), []])
    def test_invalid_data(self, data):
        with pytest.raises(ParseError):
            NotificationImplementationDefinition.normalize(Node(data))

    def test_string_normalization(self):
        obj = NotificationImplementationDefinition.normalize(Node("string"))

        assert obj.bare == {"primary": "string"}

    def test_dict_normalization(self):
        node = Node({})
        obj = NotificationImplementationDefinition.normalize(node)

        assert obj == node


class TestParse:
    def test_full(self, yaml_ast):
        NotificationImplementationDefinition.parse(yaml_ast(
            # language=yaml
            """
            primary: first
            dependencies:
              - second
            """
        ))

    def test_minimal(self, yaml_ast):
        NotificationImplementationDefinition.parse(yaml_ast("first"))
