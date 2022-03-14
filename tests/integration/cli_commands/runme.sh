#!/bin/bash
set -euo pipefail

# get opera-tosca-parser executable
opera_tosca_parser_executable="$1"

# perform an integration test for most important opera-tosca-parser CLI commands and their options
# prepare the TOSCA CSAR zip file
zip -r test.csar service.yaml playbooks TOSCA-Metadata

# parse TOSCA service template and TOSCA CSAR (with JSON/YAML inputs)
$opera_tosca_parser_executable parse --inputs inputs.json service.yaml
$opera_tosca_parser_executable parse --inputs inputs.yaml test.csar

# remove the created zip
rm -f test.csar
