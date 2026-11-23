#!/bin/bash
# Run the bot against the SC2 client started by launch_sc2.sh.
# Usage: ./run_bot.sh [extra bot.py args]
#   e.g. ./run_bot.sh --race terran --opponent-race zerg --difficulty medium
set -euo pipefail
cd "$(dirname "$0")"

# python-sc2 ships protobuf stubs older than protobuf>=4; force pure-python impl.
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

if [ ! -x .venv/bin/python ]; then
  echo "No .venv here. First time setup:"
  echo "  python3 -m venv .venv && .venv/bin/pip install sc2"
  exit 1
fi

exec .venv/bin/python bot.py "$@"
