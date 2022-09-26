import importlib
from pathlib import PurePath, Path

from opera_tosca_parser.error import ParseError
from opera_tosca_parser.parser import yaml
from opera_tosca_parser.parser.tosca.v_1_3 import stdlib
from opera_tosca_parser.parser.tosca.v_2_0 import Parser
from opera_tosca_parser.parser.tosca.v_2_0 import ServiceTemplate
from opera_tosca_parser.parser.tosca.v_2_0 import profiles
from opera_tosca_parser.parser.utils.location import Location
from opera_tosca_parser.parser.yaml.node import Node

# TODO: Should we remove support for TOSCA v1.3 when TOSCA 2.0 officially becomes a standard?
# This is a dict with name of TOSCA version as key and relative path to parser definitions as value
SUPPORTED_TOSCA_VERSIONS = dict(
    tosca_simple_yaml_1_3="v_1_3",
    tosca_2_0="v_2_0"
)


def _get_tosca_version(input_yaml: Node) -> str:
    """
    Get TOSCA version for TOSCA service template
    :param input_yaml: YAML Node input for TOSCA service template
    :return: TOSCA version string
    """
    for k, v in input_yaml.value.items():
        if k.value == "tosca_definitions_version":
            try:
                return SUPPORTED_TOSCA_VERSIONS[v.value]
            except (TypeError, KeyError) as e:
                raise ParseError(
                    f"Unsupported TOSCA version. Available: {', '.join(SUPPORTED_TOSCA_VERSIONS.keys())}.", v.loc
                ) from e

    raise ParseError("Missing TOSCA version.", input_yaml.loc)


def _get_parser(tosca_version: str) -> Parser:
    """
    Get parser for TOSCA service template
    :param tosca_version: TOSCA version
    :return: Parser object
    """
    return importlib.import_module(f".{tosca_version}", __name__).Parser  # type: ignore


def load(base_path: Path, service_template: PurePath) -> ServiceTemplate:
    """
    Load TOSCA service template
    :param base_path: Base path to workdir where TOSCA service template is located
    :param service_template: Path to TOSCA service template
    :return: Loaded TOSCA service template as dictionary
    """
    with (base_path / service_template).open() as input_fd:
        input_yaml = yaml.load(input_fd, str(service_template))
    if not isinstance(input_yaml.value, dict):
        raise ParseError("Top level structure should be a map.", Location(str(service_template), 0, 0))

    tosca_version = _get_tosca_version(input_yaml)
    parser = _get_parser(tosca_version)

    if tosca_version == "v_2_0":
        service = parser.parse_service_template(input_yaml, base_path, service_template, set())[0]
    else:
        stdlib_yaml = stdlib.load(tosca_version)
        service = parser.parse_service_template(stdlib_yaml, base_path, PurePath("STDLIB"), set())[0]
        service.merge(parser.parse_service_template(input_yaml, base_path, service_template, set())[0])

    service.visit("resolve_path", base_path)
    service.visit("resolve_reference", service)

    return service
