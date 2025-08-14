#!/usr/bin/env bash
# This script removes ADRift and its dependencies in a Kubernetes cluster.

set -eou pipefail

echo "[INFO] - Removing ADRift and its dependencies..."
kubectl get pods -n adrift | awk '{print $1}' | grep -v NAME | xargs -r kubectl delete pod -n adrift > /dev/null 2>&1 || true

# Let's remove ADRift
echo "[INFO] - Removing Postgres Persistent Volume/Claim..."
kubectl delete pv postgres-pv -n adrift > /dev/null 2>&1 || true
kubectl delete pvc postgres-pvc -n adrift > /dev/null 2>&1 || true

echo "[INFO] - Removing 'adrift' namespace..."
kubectl delete namespace adrift > /dev/null 2>&1 || true

kubectl delete application adrift -n argocd > /dev/null 2>&1 || true
echo "[INFO] - Removed ADRift and its dependencies..."
