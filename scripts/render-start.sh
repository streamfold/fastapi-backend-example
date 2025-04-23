#!/bin/bash

CWD="$(cd -P -- "$(dirname -- "$0")" && pwd -P)"

set -e

cd $CWD/.. && source .venv/bin/activate

PORT=${PORT:-10000}

exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT" --workers 2
