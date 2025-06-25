# Build A Docker Image for PyFlowOps

This document details how to buiLd a Docker image for your application _(within your repos created with the `pfo CLI`)_.

## Setup

In order for the PyFlowOps automation to pickup your Docker images for `builds`|`deployments`, you need to create the Docker scripts, files, etc. in the <repo>/docker/<image_name> folder.

## Scanning

The `pfo CLI` will scan these repos if it is annotated in the `pfo.json`. This means that the repo must be registered and tracked with the PyFlowOps CLI tool. To install the `pfo CLI` - Please see the [pfo CLI Installation](pfo-cli/index.md#installation).

## Directory Structure

In order for the PyFlowOps automation to work correctly, and build the Docker images that are defined in
the `pfo.json`, they must follow the directory structure below:

`<repo>/docker/<image_name>/Dockerfile>`

**IMPORTANT**: You can have multiple Docker images in a repo, as long as they are in this format.

## Adding Dockerfiles, CI/CD to pfo.json

For the `pfo CLI` to scan and register your Dockerfile as part of the Kubernetes build/deployment process,
you need to add your Docker information to the `pfo.json` file.

If you do NOT have a "docker" key within the pfo.json file, you will need to create one that acts as the 
highest level key for all docker builds from your repo.

Example:

```json
"docker": {
  "docs": {
      "image": "ghcr.io/pyflowops/documentation",
      "base_path": "docker",
      "repo_path": "docker/docs",
      "dockerfile": "Dockerfile"
  }
}
```
  