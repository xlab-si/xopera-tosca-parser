from opera_tosca_parser.parser.yaml.node import Node

from ..entity import Entity
from ..string import String


class RepositoryDefinition(Entity):
    ATTRS = dict(
        description=String,
        url=String
    )
    REQUIRED = {"url"}

    @classmethod
    def normalize(cls, yaml_node: Node) -> Node:
        """
        Normalize RepositoryDefinition object
        :param yaml_node: YAML node
        :return: Normalized Node object
        """
        if not isinstance(yaml_node.value, (str, dict)):
            cls.abort("Invalid repository data. Expected string or dict.", yaml_node.loc)
        if isinstance(yaml_node.value, str):
            return Node({Node("url"): yaml_node})
        return yaml_node
