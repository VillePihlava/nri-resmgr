#!/usr/bin/env bash

SCRIPT_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

export NUMBER_OF_REPLICAS="1"
USE_PROMETHEUS="false"

usage () {
    echo "usage: $0 -n <number of stress-ng pods> -p <use prometheus: \"true\" or \"false\">"
    exit 1
}

while getopts ":n:p:" option; do
    case ${option} in
        n) 
            NUMBER_OF_REPLICAS="${OPTARG}"
            ;;
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

# Create correct amount of stress-ng replicas
envsubst < "${SCRIPT_DIR}/manifests/stress-ng-deployment.yaml" | kubectl apply -f -
