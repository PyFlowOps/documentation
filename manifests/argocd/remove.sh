#!/usr/bin/env bash
# This script removes ADRift and its dependencies in a Kubernetes cluster.

set -eou pipefail

echo "[INFO] - Removing Documentation and its dependencies..."

# Let's remove Documentation application
echo "[INFO] - Removing 'pyops-docs' namespace..."
kubectl delete namespace pyops-docs > /dev/null 2>&1 || true

kubectl delete application docs -n argocd > /dev/null 2>&1 || true
echo "[INFO] - Removed Documentation and its dependencies..."
