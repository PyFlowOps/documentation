#!/usr/bin/env bash
# This script installs ADRift and its dependencies in a Kubernetes cluster.

set -eou pipefail

# This script assumes that kubectl and kustomize are installed and configured.
# Namespace installation
[[ $(kubectl get namespace pyops-docs 2>/dev/null) ]] || {
    echo "[INFO] - Creating 'pyops-docs' namespace..."
    kubectl apply -f namespace.yaml
}

# Check if the namespace was created successfully
echo "[INFO] - Installing Documentation pip requirements..."
python -m pip install -r scripts/requirements.txt > /dev/null 2>&1 || true

if [[ $? -ne 0 ]]; then
    echo "[ERROR] - Failed to render Documentation application patches. Please check the script output."
    exit 1
fi

# Let's get the prerequisites ready
echo "[INFO] - Installing prerequisites..."
python scripts/github-ssh.py # This sets up the SSH keys for GitHub access
sleep 1

# Install Documentation application
echo "[INFO] - Installing Documentation application..."
kustomize build overlays | kubectl apply -f - > /dev/null 2>&1 || true
sleep 3

echo "[COMPLETE] - Documentation application and its dependencies have been successfully installed!"
