import pytest

from opera_tosca_parser.parser.tosca.v_2_0.definitions.data_type import DataType
from opera_tosca_parser.parser.yaml.node import Node


class TestNormalize:
    @pytest.mark.parametrize("data", [1, 2.3, True, (), "string"])
    def test_ignores_non_dict_data(self, data):
        node = Node(data)

        assert DataType.normalize(node) == node

    def test_ignores_dict_data_with_derived_from_key(self):
        node = Node({Node("derived_from"): Node("integer")})

        assert DataType.normalize(node) == node

    def test_updates_dict_data_with_derived_from_key(self):
        assert DataType.normalize(Node({})).bare == {"derived_from": "None"}


class TestParse:
    def test_full(self, yaml_ast):
        DataType.parse(yaml_ast(
            # language=yaml
            """
            derived_from: data_type
            description: My desc
            metadata:
              key: value
            version: "1.4"
            constraints:
              - in_range: [ 1, 6 ]
            properties:
              prop:
                type: map
            """
        ))

    def test_minimal(self, yaml_ast):
        DataType.parse(yaml_ast("{}"))
