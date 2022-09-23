from typing import Dict, Any, List as Lst

from opera_tosca_parser.parser.tosca.v_2_0.template.node import Node
from opera_tosca_parser.parser.tosca.v_2_0.template.requirement import Requirement
from .artifact_definition import ArtifactDefinition
from .capability_assignment import CapabilityAssignment
from .collector_mixin import CollectorMixin  # type: ignore
from .interface_assignment import InterfaceAssignment
from .node_filter_definition import NodeFilterDefinition
from .relationship_template import RelationshipTemplate
from .requirement_assignment import RequirementAssignment
from ..list import List
from ..map import Map
from ..reference import Reference
from ..string import String
from ..void import Void


# NOTE: We deviate form the TOSCA standard in attribute assignment statement, since the official grammar is just
# ridiculous (it makes assigning complex values impossible in simplified form).


class NodeTemplate(CollectorMixin):
    ATTRS = dict(
        type=Reference("node_types"),
        description=String,
        metadata=Map(String),
        directives=List(String),
        properties=Map(Void),
        attributes=Map(Void),
        requirements=List(Map(RequirementAssignment)),
        capabilities=Map(CapabilityAssignment),
        interfaces=Map(InterfaceAssignment),
        artifacts=Map(ArtifactDefinition),
        node_filter=NodeFilterDefinition,
        copy=Reference("topology_template", "node_templates"),
    )
    REQUIRED = {"type"}

    def get_template(self, name: str, service_ast: Dict[str, Any]) -> Node:
        """
        Get Node object from template
        :param name: Node name
        :param service_ast: Abstract syntax tree dict
        :return: Node object
        """
        return Node(
            name=name,
            types=self.collect_types(service_ast),
            properties=self.collect_properties(service_ast),
            attributes=self.collect_attributes(service_ast),
            requirements=self.collect_requirements(name, service_ast),
            capabilities=self.collect_capabilities(service_ast),
            interfaces=self.collect_interfaces(service_ast),
            artifacts=self.collect_artifacts(service_ast),
        )

    # Next function is not part of the CollectorMixin, because requirements are node template only thing.
    def collect_requirements(self, node_name: str, service_ast: Dict[str, Any]) -> Lst[Requirement]:
        """
        Collect requirements for node template
        :param node_name: Node name
        :param service_ast: Abstract syntax tree dict
        :return: List of requirements
        """
        typ = self.type.resolve_reference(service_ast)
        definitions = typ.collect_requirement_definitions(service_ast)

        requirements = []
        undeclared_requirements = set()
        for req in self.get("requirements", {}):
            (name, assignment), = req.items()
            if name not in definitions:
                undeclared_requirements.add(name)
                continue

            if not assignment.dig("node"):
                self.abort("Opera does not support abstract requirements", assignment.loc)

            # Validate node template reference
            assignment.node.resolve_reference(service_ast)

            relationship_ref = assignment.get("relationship")
            if relationship_ref:
                relationship = relationship_ref.resolve_reference(service_ast)
                relationship_name = relationship_ref.data
            else:
                # Create an anonymous relationship template of the right type
                relationship = RelationshipTemplate(dict(type=definitions[name].relationship), None)
                relationship_name = f"{node_name}-{name}-{assignment.node.data}"

            count_range = definitions[name].get("count_range")

            requirements.append(
                Requirement(
                    name, assignment.node.data, relationship.get_template(relationship_name, service_ast), count_range
                )
            )

        if undeclared_requirements:
            self.abort(f"Undeclared requirements: {', '.join(undeclared_requirements)}.", self.loc)

        # detect missing requirements based on their occurrences
        missing_requirements = set()
        for req in definitions.keys() - {req.name for req in requirements}:
            count_range = definitions[req].get("count_range")
            optional = definitions[req].get("optional", False)
            if not optional and not count_range or (count_range and count_range.data[0] > 0):
                missing_requirements.add(req)

        if missing_requirements:
            self.abort(f"Missing requirements: {', '.join(missing_requirements)}.", self.loc)

        return requirements
