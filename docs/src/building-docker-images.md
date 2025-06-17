# Build A Docker Image for PyFlowOps

This document details how to buiLd a Docker image for your application _(within your repos created with the `pfo CLI`)_.

## Setup

In order for the PyFlowOps automation to pickup your Docker images for `builds`|`deployments`, you need to create the Docker scripts, files, etc. in the <repo>/docker/<image_name> folder.

## Scanning

The `pfo CLI` will scan these repos if it is annotated in the `pfo.json`. This means that the repo must be registered and tracked with the PyFlowOps CLI tool. To install the `pfo CLI` - Please see the [pfo CLI Installation](http://localhost:8100/src/pfo-cli/#installation).

## Directory Structure

In order for the PyFlowOps automation to work correctly, and build the Docker images that are defined in
the `pfo.json`, they must follow the directory structure below:

`<repo>/docker/<image_name>/Dockerfile>`

**IMPORTANT**: You can have multiple Docker images in a repo, as long as they are in this format.
