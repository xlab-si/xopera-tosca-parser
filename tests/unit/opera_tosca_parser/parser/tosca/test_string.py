import pytest

from opera_tosca_parser.error import ParseError
from opera_tosca_parser.parser.tosca.string import String
from opera_tosca_parser.parser.yaml.node import Node


class TestValidate:
    def test_with_string_data(self):
        String.validate(Node("string"))

    @pytest.mark.parametrize("data", [4, (), (1, 2, 3), [], ["a", "b"], {}])
    def test_with_non_string(self, data):
        with pytest.raises(ParseError):
            String.validate(Node(data))
