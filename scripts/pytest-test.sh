#!/bin/bash

if [ -f api/.env ]; then
    export $(grep -v '^#' api/.env | xargs)
fi

pytest -n auto -s -c pytest.ini -vv
