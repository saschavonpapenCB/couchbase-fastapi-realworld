#!/bin/bash
docker run -it --env-file api/.env -p 8000:8000 couchbase-fastapi-realworld