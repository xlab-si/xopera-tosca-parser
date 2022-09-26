import pytest

from opera_tosca_parser.error import ParseError
from opera_tosca_parser.parser.tosca.v_2_0.definitions.constraint_clause import ConstraintClause


class TestValidate:
    def test_valid_clause(self, yaml_ast):
        ConstraintClause.validate(yaml_ast("equal: 3"))

    def test_invalid_clause(self, yaml_ast):
        with pytest.raises(ParseError):
            ConstraintClause.validate(yaml_ast("bad_operator: must fail"))


class TestParse:
    def test_parse(self, yaml_ast):
        ConstraintClause.parse(yaml_ast("in_range: [ 1, 2 ]"))
