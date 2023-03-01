#!/usr/bin/env bash

SCRIPT_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

kubectl delete -f "${SCRIPT_DIR}/manifests/stress-ng-deployment.yaml"

helm uninstall -n monitoring prometheus
