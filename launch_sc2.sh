#!/bin/bash
# Launch StarCraft II on macOS in Remote Control mode for the bot.
# Prereq: Battle.net app + SC2 installed, and you have logged in once manually
# with the account below (free-to-play account is fine).
set -euo pipefail

ACCOUNT="${SC2_ACCOUNT:?set SC2_ACCOUNT=your-battlenet-email}"

open -a StarCraft --args \
  --port=5000 \
  --start-port=5001 \
  --request-port=5002 \
  --windowed \
  --windowed-width=128 \
  --windowed-height=128 \
  --full-minimize \
  --add-account="$ACCOUNT"

echo "SC2 launching in remote-control mode on port 5000."
echo "Wait until it sits at the main menu, then run: ./run_bot.sh"
