# PyFlowOps Documentation

This is the repo for the PyFlowOps documentation website.

## Getting Started

This documentation site uses MkDocs to generate the static site. To get started, you will need to install MkDocs and the Material theme.

### Prerequisites

- Python 3.12^ or higher 
- MkDocs

### Installing

To install MkDocs, run the following command:

```bash
pip install -r requirements.txt
```

### Testing changes to other repository's documentation - IMPORTANT

If you are making changes to another repository's documentation, you will need to clone that repository and make your changes there. Once you have made your changes, you will need to build the documentation manually. In the `/scripts`, the
repos are all pulled down and built from the `main` branches. If you are adding new documentation in other repositories and want to ensure that the links work correctly, etc. you will need to pull the repo down by the branch and build it manually.

The `docs.sh` script in the `/scripts` directory will pull down the repos and build them for you. In the script are the lines of code specifying which repos to pull down and build. You will need to add the repo to the script and run it to build the documentation.

Example:

```bash
############################ PyFlowOps Repo ############################
#git clone --branch feat/<your-branch-name> https://github.com/pyflowops/base-repo-template.git "${BASEDIR}"/temp/base-repo-template # Clone the base-repo-template repo
git clone --branch main https://github.com/pyflowops/base-repo-template.git "${BASEDIR}"/temp/base-repo-template

# Make the dirs for POCs
# Example
mkdir -p "${BASEDIR}"/docs/src/poc
```

As you can see in the above repo, the `feat/<your-branch-name>` branch is being pulled down and built. You will need to add the repo and branch to the script and run it to build the documentation with the documentation changes in the other repository.
