import pytest

from opera_tosca_parser.error import ParseError
from opera_tosca_parser.parser.tosca.bool import Bool
from opera_tosca_parser.parser.yaml.node import Node


class TestValidate:
    @pytest.mark.parametrize("data", [True, False])
    def test_with_bool_data(self, data):
        Bool.validate(Node(data))

    @pytest.mark.parametrize(
        "data", [4, (), (1, 2, 3), [], ["a", "b"], {}],
    )
    def test_with_non_bool_data(self, data):
        with pytest.raises(ParseError):
            Bool.validate(Node(data))
