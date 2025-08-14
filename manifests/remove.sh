#!/usr/bin/env bash
# This script removes ADRift and its dependencies in a Kubernetes cluster.

set -eou pipefail

echo "[INFO] - Removing PyOps-Docs and its dependencies..."
kubectl get pods -n pyops-docs | awk '{print $1}' | grep -v NAME | xargs -r kubectl delete pod -n pyops-docs > /dev/null 2>&1 || true

echo "[INFO] - Removing 'pyops-docs' namespace..."
kubectl delete namespace pyops-docs > /dev/null 2>&1 || true
