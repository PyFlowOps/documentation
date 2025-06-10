#!/bin/bash
# Author - Philip De Lorenzo

# This script retrieves the current Poetry tag and compares it to what is in Git
# and if the Git tags are not equal, then the logic assumes that the tag must be
# added to Github and does as such.
#
# This tagging script is for single repo Poetry libraries.

set -eou pipefail

NAME="pyflowops/docs"
VERSION="latest"
TAG="${NAME}/v${VERSION}"

if [[ -z "${CI}" ]] || [[ -z "${GITHUB_ACTIONS}" ]]; then
    echo "[ERROR] - Script is to be run within Github Actions only."
    exit 1
# This is set to check both variables as a means of ensuring that the script cannot run unless it is a github environment
elif [[ ! -z "${CI}" ]] && [[ ! -z "${GITHUB_ACTIONS}" ]]; then
    git tag -a ${TAG} --force -m "Versioning pyflowops/docs Automation ~> ${TAG}"
    git push origin ${TAG}
fi
