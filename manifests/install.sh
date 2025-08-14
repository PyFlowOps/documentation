#!/usr/bin/env bash
# This script installs ADRift and its dependencies in a Kubernetes cluster.

set -eou pipefail

# This script assumes that kubectl and kustomize are installed and configured.
# Namespace installation
kubectl apply -f namespace.yaml

# Check if the namespace was created successfully
python -m pip install -r scripts/requirements.txt
python scripts/patch-render.py # This gets the environment variables set up correctly for the ADRift application

python scripts/secret-render.py --aws # This renders the ADRift secret file with the correct values | this project uses AWS credentials
python scripts/docker-login.py --aws # This logs into the AWS ECR registry
sleep 1
python scripts/docker-download.py --aws # This downloads the Docker image from ECR
sleep 1
python scripts/github-ssh.py # This sets up the SSH keys for GitHub access

if [[ $? -ne 0 ]]; then
    echo "[ERROR] - Failed to render ADRift application patches. Please check the script output."
    exit 1
fi

# Install Docs
echo "[INFO] - Installing PyOps-Docs..."
cd pyops-docs || exit 1 && kustomize build overlays | kubectl apply -f - > /dev/null 2>&1 || true
sleep 3

echo "[COMPLETE] - PyOps-Docs and its dependencies have been successfully installed!"
