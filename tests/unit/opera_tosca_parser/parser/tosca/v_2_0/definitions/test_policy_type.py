from opera_tosca_parser.parser.tosca.v_2_0.definitions.policy_type import PolicyType


class TestParse:
    def test_full(self, yaml_ast):
        PolicyType.parse(yaml_ast(
            # language=yaml
            """
            derived_from: policy_type
            description: My desc
            metadata:
              key: value
            version: "1.2"
            properties: {}
            targets: [ node_type, group_type ]
            triggers:
              my_trigger:
                description: A trigger
                event: my_trigger
                target_filter:
                  node: node
                  requirement: my_requirement
                  capability: my_capability
                condition:
                  constraint:
                    - not:
                      - and:
                        - my_attribute: [ in_range: [1, 50] ]
                        - my_other_attribute: [ equal: my_other_value ]
                  period: 60 sec
                  evaluations: 2
                  method: average
                action:
                  - call_operation:
                      operation: test.interfaces.test.Test.test
                      inputs:
                        test_input: { get_property: [ SELF, test_property ] }
                  - delegate:
                      workflow: delegate_workflow_name
                      inputs:
                        test_input: { get_input: [ SELF, test_input ] }
            """
        ))

    def test_minimal(self, yaml_ast):
        PolicyType.parse(yaml_ast(
            # language=yaml
            """
            derived_from: policy_type
            """
        ))
