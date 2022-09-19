from opera_tosca_parser.parser.tosca.v_1_3.definitions.credential import Credential


class TestParse:
    def test_full(self, yaml_ast):
        Credential.parse(yaml_ast(
            # language=yaml
            """
            protocol: tcp
            token_type: password
            token: my_password
            keys:
              first: key
              yet: another key
            user: my_user
            """
        ))

    def test_minimal(self, yaml_ast):
        Credential.parse(yaml_ast(
            # language=yaml
            """
            token: my_password
            """
        ))
