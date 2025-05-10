#!/usr/bin/env bash

set -eo pipefail

BASE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BASEDIR="$( realpath "${BASE}/..")"
TEMPDIR="${BASEDIR}/temp"

# Add the folder to the array if this item is to be cleaned on service init
CLEAN_FOLDERS=( "docs" "temp" "docker" "iac" )

# Getting Documentation from other repos
# We need to remove any 
if [[ -d "${BASEDIR}/temp" ]]; then
  rm -rf "${BASEDIR}/temp"
fi

mkdir -p "${BASEDIR}"/temp # Make the temp directory for all data to be stored

# Cleaning the docs folder
for i in "${CLEAN_FOLDERS[@]}"; do
  if [[ -d "${BASEDIR}/docs/src/${i}" ]]; then
    rm -rf "${BASEDIR}/docs/src/${i}"
  fi
done

### Local ###
# Make the needed directories
mkdir -p "${BASEDIR}"/docs/src/docker

# Make the dirs for the cloud functions (ALL)
mkdir -p "${BASEDIR}"/docs/src/cloud-functions

cp -R "${BASEDIR}"/docker/* "${BASEDIR}"/docs/src/docker

############################ Manscaped SRE Repo ############################
#git clone --branch feat/sre-gcp https://github.com/manscaped-dev/manscaped-sre.git "${BASEDIR}"/temp/manscaped-sre # Clone the manscaped-sre repo
git clone --branch main https://github.com/pyflowops/base-repo-template.git "${BASEDIR}"/temp/base-repo-template

# Copying the Architecture Decision Records from the manscaped-sre repo
#cp -R "${TEMPDIR}"/manscaped-sre/doc/adr "${BASEDIR}"/docs/src # Copy the ADRs to the docs folder directly

# Make the dirs for the dev portal (manscaped-sre repo)
#mkdir -p "${BASEDIR}"/docs/src/repo_additions

# Copying the docs from the manscaped-sre repo
#cp -R "${TEMPDIR}"/manscaped-sre/sre_portal/* "${BASEDIR}"/docs/src/manscaped-sre/sre_portal
#cp -R "${TEMPDIR}"/manscaped-sre/docs/index.md "${BASEDIR}"/docs/src/manscaped-sre # This is in it's own folder
#cp -R "${TEMPDIR}"/manscaped-sre/docs/developer-mac-setup.md "${BASEDIR}"/docs/src # This is in the main root folder /src
#cp -R "${TEMPDIR}"/manscaped-sre/docs/dev-mac-img "${BASEDIR}"/docs/src # This is in the main root folder /src
#cp -R "${TEMPDIR}"/manscaped-sre/poc/* "${BASEDIR}"/docs/src/poc # This is in it's own folder 
#cp -R "${TEMPDIR}"/manscaped-sre/docker "${BASEDIR}"/docs/src/docker/manscaped-sre # rundeck docker image
#cp -R "${TEMPDIR}"/manscaped-sre/mnscpd-app-docker "${BASEDIR}"/docs/src # mnscpd-app-docker docker image
#cp -R "${TEMPDIR}"/manscaped-sre/docker/datadog-agent "${BASEDIR}"/docs/src/docker/datadog-agent # datadog-agent docker image
#############################################################################

############################ Manscaped SRE Deployments Repo ############################
#git clone --branch main https://github.com/manscaped-dev/manscaped-sre-deployments.git "${BASEDIR}"/temp/manscaped-sre-deployments # Clone the manscaped-sre-deployments repo

# Make the dirs for the deployments
#mkdir -p "${BASEDIR}"/docs/src/manscaped-sre-deployments

# Copying the docs from the manscaped-sre-deployments repo
#cp -R "${TEMPDIR}"/manscaped-sre-deployments/docs/* "${BASEDIR}"/docs/src/manscaped-sre-deployments

#########################################################################################

############################ Manscaped SRE Github Actions Repo(s) ############################

#git clone --branch main https://github.com/manscaped-dev/sre-gha-build-push "${BASEDIR}"/temp/sre-gha-build-push
#git clone --branch main https://github.com/manscaped-dev/sre-gha-cloudrun-deploy "${BASEDIR}"/temp/sre-gha-cloudrun-deploy

# Make the dirs for the deployments
#mkdir -p "${BASEDIR}"/docs/src/sre-gha-build-push
#mkdir -p "${BASEDIR}"/docs/src/sre-gha-cloudrun-deploy

# Copying the docs from the manscaped-sre-deployments repo
#cp -R "${TEMPDIR}"/sre-gha-build-push/README.md "${BASEDIR}"/docs/src/sre-gha-build-push/index.md
#cp -R "${TEMPDIR}"/sre-gha-cloudrun-deploy/README.md "${BASEDIR}"/docs/src/sre-gha-cloudrun-deploy/index.md

##############################################################################################

############################ Manscaped SRE Mando ############################
#git clone --branch prod https://github.com/manscaped-dev/mando "${BASEDIR}"/temp/mando

# Make the dirs for the deployments
#mkdir -p "${BASEDIR}"/docs/src/mando

# Copying the docs from the manscaped-sre-deployments repo
#cp -R "${TEMPDIR}"/mando/README.md "${BASEDIR}"/docs/src/mando/index.md
#cp -R "${TEMPDIR}"/mando/img "${BASEDIR}"/docs/src/mando
#cp -R "${TEMPDIR}"/mando/docs "${BASEDIR}"/docs/src/mando
#############################################################################

############################ Manscaped SRE Cloud Functions ############################
#git clone --branch main https://github.com/manscaped-dev/mnscpd-sre-cloud-functions "${BASEDIR}"/temp/cloud-functions/sre

# Make the dirs for the deployments
#mkdir -p "${BASEDIR}"/docs/src/cloud-functions/sre

# Copying the docs from the manscaped-sre-deployments repo
#cp -R "${TEMPDIR}"/cloud-functions/sre/* "${BASEDIR}"/docs/src/cloud-functions/sre
#############################################################################

############################ Manscaped Laptop Setup Documentation ############################
#git clone --branch main git@github.com:manscaped-dev/mnscpd-mac-setup.git "${BASEDIR}"/temp/mnscpd-mac-setup

# Make the dirs for the deployments
#mkdir -p "${BASEDIR}"/docs/src/mnscpd-mac-setup

# Copying the docs from the manscaped-sre-deployments repo
#cp -R "${TEMPDIR}"/mnscpd-mac-setup/docs/* "${BASEDIR}"/docs/src/mnscpd-mac-setup
#############################################################################


#git clone --branch main https://github.com/manscaped-dev/manscaped-infrastructure.git ${BASEDIR}/temp/manscaped-infrastructure

### Creating the Documentation ###


# Copying the documentation from the manscaped-sre repo
#cp -R ${TEMPDIR}/manscaped-cli/docs ${BASEDIR}/docs/src/manscaped-cli
#cp -R ${TEMPDIR}/manscaped-sre-automation/docs ${BASEDIR}/docs/src/manscaped-sre-automation
#cp -R ${TEMPDIR}/manscaped-infrastructure/docs ${BASEDIR}/docs/src/manscaped-infrastructure
#cp -R ${TEMPDIR}/manscaped-sre-third-party-status/docs ${BASEDIR}/docs/src/manscaped-sre-third-party-status

# Get the documentation needed from the Manscaped SRE repo
#cp -R ${TEMPDIR}/manscaped-sre/dev_portal/README.md ${BASEDIR}/docs/src/dev_portal
#cp -R ${TEMPDIR}/manscaped-sre/dev_portal/frontend/README.md ${BASEDIR}/docs/src/dev_portal/frontend
#cp -R ${TEMPDIR}/manscaped-sre/dev_portal/frontend/docs docs/src/dev_portal/frontend
#cp -R ${TEMPDIR}/manscaped-sre/dev_portal/backend/README.md ${BASEDIR}/docs/src/dev_portal/backend
#cp -R ${TEMPDIR}/manscaped-sre/dev_portal/backend/docs ${BASEDIR}/docs/src/dev_portal/backend

# Let's get all of the cloud function information
#items=( "$(ls ${TEMPDIR}/manscaped-sre/cloud_functions)" )
#for i in "${items[@]}"; do
#  if [ -d "${TEMPDIR}/manscaped-sre/cloud_functions/${i}" ]; then
#    mkdir -p ${BASEDIR}/docs/src/cloud_functions/${i}
#    cp -R ${TEMPDIR}/manscaped-sre/cloud_functions/${i}/README.md ${BASEDIR}/docs/src/cloud_functions/${i}
#    if [ -d "${TEMPDIR}/manscaped-sre/cloud_functions/${i}/docs" ]; then
#      cp -R ${TEMPDIR}/manscaped-sre/cloud_functions/${i}/docs ${BASEDIR}/docs/src/cloud_functions/${i}
#    fi
#  fi
#done
