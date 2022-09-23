import pytest

from opera_tosca_parser.error import ParseError
from opera_tosca_parser.parser.tosca.v_2_0.definitions.operation_host import OperationHost
from opera_tosca_parser.parser.yaml.node import Node


class TestValidate:
    @pytest.mark.parametrize(
        "version", ["SELF", "SOURCE", "TARGET", "ORCHESTRATOR"]
    )
    def test_valid_tosca_versions(self, version):
        OperationHost.validate(Node(version))

    @pytest.mark.parametrize(
        "version", ["", "  ", "a", "tosca_2_0", 123, "abc", {}, []]
    )
    def test_invalid_tosca_versions(self, version):
        with pytest.raises(ParseError):
            OperationHost.validate(Node(version))
