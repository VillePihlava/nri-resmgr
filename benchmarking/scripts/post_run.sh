#!/usr/bin/env bash

# Draw graphs

SCRIPT_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
BASE_DIR="$(realpath "${SCRIPT_DIR}/..")"

python3 plot-graphs.py -o "${BASE_DIR}/output/traces.png" -l "topology-aware-jaeger,baseline-jaeger" "${BASE_DIR}/output"
python3 plot-graphs.py -o "${BASE_DIR}/output/resource_usage.png" -l "topology-aware-prometheus,baseline-prometheus" "${BASE_DIR}/output"
