#!/usr/bin/env bash

# Currently only for deploying Prometheus.

SCRIPT_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
BASE_DIR="$(realpath "${SCRIPT_DIR}/..")"

USE_PROMETHEUS="false"

usage () {
    echo "usage: $0 -p <use prometheus: \"true\" or \"false\">"
    exit 1
}

while getopts ":n:p:" option; do
    case ${option} in
        p)
            USE_PROMETHEUS="${OPTARG}"
            if [ "${OPTARG}" != "true" ] && [ "${OPTARG}" != "false" ]; then
                usage
            fi
            ;;
        \?)
            usage
    esac
done

if [ "${USE_PROMETHEUS}" == "true" ]; then
    helm install prometheus prometheus-community/prometheus --version 19.7.2 -f prometheus-values.yaml --namespace monitoring --create-namespace
fi
