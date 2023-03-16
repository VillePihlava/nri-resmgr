#!/usr/bin/env bash

# For running incremental test where containers are first deployed in the amount of increments, and then destroyed in the amount of increments.

SCRIPT_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
BASE_DIR="$(realpath "${SCRIPT_DIR}/..")"

NUMBER_OF_CONTAINERS_IN_INCREMENT="1"
NUMBER_OF_INCREMENTS="1"

usage () {
    echo "usage: $0 -n <number of stress-ng containers in increment> -i <increments>"
    exit 1
}

while getopts ":n:i:" option; do
    case ${option} in
        n) 
            NUMBER_OF_CONTAINERS_IN_INCREMENT="${OPTARG}"
            ;;
        i)
            NUMBER_OF_INCREMENTS="${OPTARG}"
            ;;
        \?)
            usage
    esac
done

START_TIME=$(date +%s)

# Loop for creating containers in increments.
for ((i = 1; i <= ${NUMBER_OF_INCREMENTS}; i++));
do
    # Adjust amount of stress-ng replicas.
    export NUMBER_OF_REPLICAS=$((NUMBER_OF_CONTAINERS_IN_INCREMENT * i))
    echo "creation iteration ${i}, adjusting containers to ${NUMBER_OF_REPLICAS}"
    envsubst < "${BASE_DIR}/manifests/stress-ng-deployment.yaml" | kubectl apply -f -
    kubectl rollout status deployment stress-ng
done

# Loop for destroying containers in increments.
for ((i = ${NUMBER_OF_INCREMENTS} - 1; i >= 0; i--));
do
    # Adjust amount of stress-ng replicas.
    export NUMBER_OF_REPLICAS=$((NUMBER_OF_CONTAINERS_IN_INCREMENT * i))
    echo "destruction iteration ${i}, adjusting containers to ${NUMBER_OF_REPLICAS}"
    envsubst < "${BASE_DIR}/manifests/stress-ng-deployment.yaml" | kubectl apply -f -
    kubectl rollout status deployment stress-ng
done



# Save results
sleep 15s
END_TIME=$(date +%s)
sleep 15s

OUTPUT_FILE_DATE_PREFIX=$(date -u +"%Y%m%dT%H%M%SZ" -d "@${START_TIME}")
python3 get-prometheus-timeseries-data.py http://127.0.0.1:30000 -q "rate(container_cpu_usage_seconds_total{container=\"nri-resmgr-topology-aware\"}[1m])" -s "${START_TIME}" -e "${END_TIME}" -c "${BASE_DIR}/output/${OUTPUT_FILE_DATE_PREFIX}-prometheus.csv"
python3 get-jaeger-tracing-data.py http://127.0.0.1:16686 -c "${BASE_DIR}/output/${OUTPUT_FILE_DATE_PREFIX}-jaeger.csv"