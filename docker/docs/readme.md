# PyFlowOps Docker Images

This houses the Docker images that are used throughout the PyFlowOps ecosystem.

## PyFlowOps Documentation

This is the Docker image that builds the documentation from this repo for deployment
and hosting on the PyFlowOps Documentation site.

### Building the PyFlowOps Documentation for Deployment

**NOTE:** From the `/docker` directory of this repo...

Run the following command to build the image locally:

```bash
make docs-package
```

This will build a Docker image locally, you can test the instance by
running the following command:

```bash
docker run -it --rm --add-host host.docker.internal:0.0.0.0 -p 8100:8100 docs:latest
```

To push the image to the Google artifact registry, run the following command:

```bash
make docs-publish
```
