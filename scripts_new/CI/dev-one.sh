#!/bin/bash

# Defaults
ARCH=${1:-linux/amd64}
JOB=${2:-unit_tests}

act -j "$JOB" -W .github/workflows/CI.yml --env-file .env.dev --network host --container-architecture "$ARCH"
