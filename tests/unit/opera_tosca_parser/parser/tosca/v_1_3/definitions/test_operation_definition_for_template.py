import pytest

from opera_tosca_parser.error import ParseError
from opera_tosca_parser.parser.tosca.v_1_3.definitions.operation_definition_for_template import \
    OperationDefinitionForTemplate
from opera_tosca_parser.parser.yaml.node import Node


class TestNormalize:
    @pytest.mark.parametrize("data", [1, 2.3, True, (), []])
    def test_invalid_data(self, data):
        with pytest.raises(ParseError):
            OperationDefinitionForTemplate.normalize(Node(data))

    def test_string_normalization(self):
        obj = OperationDefinitionForTemplate.normalize(Node("string"))

        assert obj.bare == {"implementation": "string"}

    def test_dict_normalization(self):
        node = Node({})
        obj = OperationDefinitionForTemplate.normalize(node)

        assert obj == node


class TestParse:
    def test_full(self, yaml_ast):
        OperationDefinitionForTemplate.parse(yaml_ast(
            # language=yaml
            """
            description: Even more text
            implementation: path/to/artifact
            inputs:
              my_input: value
            outputs:
              my_output: [ SELF, attribute_name ]
            """
        ))

    def test_minimal(self, yaml_ast):
        OperationDefinitionForTemplate.parse(yaml_ast("{}"))
