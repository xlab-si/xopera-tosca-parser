from opera_tosca_parser.parser.yaml.node import Node

from .artifact_definition import ArtifactDefinition
from ..entity import Entity
from ..integer import Integer
from ..list import List


class OperationImplementationDefinition(Entity):
    ATTRS = dict(
        primary=ArtifactDefinition,
        dependencies=List(ArtifactDefinition),
        timeout=Integer
    )

    @classmethod
    def normalize(cls, yaml_node: Node) -> Node:
        """
        Normalize OperationImplementationDefinition object
        :param yaml_node: YAML node
        :return: Normalized Node object
        """
        if not isinstance(yaml_node.value, (str, dict)):
            cls.abort("Expected string or map.", yaml_node.loc)
        if isinstance(yaml_node.value, str):
            return Node({Node("primary"): yaml_node})
        return yaml_node
