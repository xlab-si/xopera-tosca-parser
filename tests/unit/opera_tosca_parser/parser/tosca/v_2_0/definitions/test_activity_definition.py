from opera_tosca_parser.parser.tosca.v_2_0.definitions.activity_definition import ActivityDefinition


class TestParse:
    def test_delegate_workflow(self, yaml_ast):
        ActivityDefinition.parse(yaml_ast(
            # language=yaml
            """
            delegate:
              workflow: delegate_workflow_name
              inputs:
                test_input: { get_input: [ SELF, test_input ] }
            """
        ))

    def test_delegate_workflow_short(self, yaml_ast):
        ActivityDefinition.parse(yaml_ast(
            # language=yaml
            """
            delegate: delegate_workflow_name
            """
        ))

    def test_set_state(self, yaml_ast):
        ActivityDefinition.parse(yaml_ast(
            # language=yaml
            """
            set_state: new_node_state
            """
        ))

    def test_call_operation(self, yaml_ast):
        ActivityDefinition.parse(yaml_ast(
            # language=yaml
            """
            call_operation:
              operation: my.interfaces.scaling.scale_up
              inputs:
                test_input: { get_input: [ SELF, test_input ] }
            """
        ))

    def test_call_operation_short(self, yaml_ast):
        ActivityDefinition.parse(yaml_ast(
            # language=yaml
            """
            call_operation: my.interfaces.scaling.scale_up
            """
        ))

    def test_inline_workflow(self, yaml_ast):
        ActivityDefinition.parse(yaml_ast(
            # language=yaml
            """
            inline:
              workflow: delegate_workflow_name
              inputs:
                test_input: { get_input: [ SELF, test_input ] }
            """
        ))

    def test_inline_workflow_short(self, yaml_ast):
        ActivityDefinition.parse(yaml_ast(
            # language=yaml
            """
            inline: delegate_workflow_name
            """
        ))
