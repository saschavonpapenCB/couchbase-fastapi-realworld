#!/bin/bash

# Default to linux/amd64
ARCH=${1:-linux/amd64}

act -W .github/workflows/CI.yml --env-file .env.stage --container-architecture "$ARCH"
