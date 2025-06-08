#!/usr/bin/env bash

set -eo pipefail

# Check if the required environment variables are set
: "${PORT:?PORT is not set}"
: "${HOST:?HOST is not set}"

python -m mkdocs serve --dev-addr=${HOST:-0.0.0.0}:${PORT:-8100}
