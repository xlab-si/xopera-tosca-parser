import pytest

from opera_tosca_parser.error import ParseError
from opera_tosca_parser.parser.tosca.integer import Integer
from opera_tosca_parser.parser.yaml.node import Node


class TestValidate:
    def test_with_int_data(self):
        Integer.validate(Node(1234))

    @pytest.mark.parametrize("data", ["4", (), (1, 2, 3), [], ["a", "b"], {}])
    def test_with_non_string(self, data):
        with pytest.raises(ParseError):
            Integer.validate(Node(data))
