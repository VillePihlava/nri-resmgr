#!/usr/bin/env bash

SCRIPT_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
BASE_DIR="$(realpath "${SCRIPT_DIR}/..")"

kubectl delete -f "${BASE_DIR}/manifests/stress-ng-deployment.yaml"
kubectl delete -f "${BASE_DIR}/manifests/jaeger-deployment.yaml"
helm uninstall -n monitoring prometheus
