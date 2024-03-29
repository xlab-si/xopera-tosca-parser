from opera_tosca_parser.parser.tosca.v_2_0.definitions.trigger_definition import TriggerDefinition


class TestParse:
    def test_full(self, yaml_ast):
        TriggerDefinition.parse(yaml_ast(
            # language=yaml
            """
            description: A trigger
            event: trigger
            target_filter:
              node: node
              requirement: my_requirement
              capability: my_capability
            condition:
              constraint:
                - not:
                  - and:
                    - my_attribute: [{equal: my_value}]
                    - my_other_attribute: [{equal: my_other_value}]
              period: 60 sec
              evaluations: 2
              method: average
            action:
              - call_operation: test.interfaces.Update.update
              - call_operation: test.interfaces.Upgrade.upgrade
            """
        ))

    def test_minimal(self, yaml_ast):
        TriggerDefinition.parse(yaml_ast(
            # language=yaml
            """
            event: trigger
            action:
              - call_operation: test.interfaces.Test.test
            """
        ))
