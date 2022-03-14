#!/bin/bash
set -euo pipefail

# get opera-tosca-parser executable
opera_tosca_parser_executable="$1"

# perform an integration test with compressed CSAR
# prepare the TOSCA CSAR zip file manually
mkdir -p csar-test
zip -r test.csar service.yaml modules TOSCA-Metadata
mv test.csar csar-test
cp inputs.yaml csar-test
cd csar-test

# parse the compressed TOSCA CSAR
$opera_tosca_parser_executable parse -i inputs.yaml test.csar

# remove the created folder
cd ..
rm -rf csar-test
