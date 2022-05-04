from __future__ import annotations

from typing import Optional, Dict, Tuple, TYPE_CHECKING

from opera_tosca_parser.error import DataError

if TYPE_CHECKING:
    from opera_tosca_parser.template.topology import Topology
    from opera_tosca_parser.template.interface import Interface
    from opera_tosca_parser.value import Value


class Relationship:
    def __init__(self, name: str, types: Tuple[str, ...], properties: Dict[str, Value], attributes: Dict[str, Value],
                 interfaces: Dict[str, Interface]):
        """
        Construct a new Relationship object
        :param name: Relationship name
        :param types: Relationship types for derivation
        :param properties: Relationship properties
        :param attributes: Relationship attributes
        :param interfaces: Relationship interfaces
        """
        self.name = name
        self.types = types
        self.properties = properties
        self.attributes = attributes
        self.interfaces = interfaces

        # This will be set when the relationship is inserted into a topology
        self.topology: Optional[Topology] = None
        # This will be set at instantiation time.
        self._instance = None  # type: ignore

    def is_a(self, typ):
        return typ in self.types

    @property
    def instance(self):
        if not self._instance:
            raise DataError(f"Relationship template {self.name} was not instantiated yet")
        return self._instance

    @instance.setter
    def instance(self, value):
        self._instance = value
