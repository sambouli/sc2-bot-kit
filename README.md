# SC2 bot kit (macOS M2)

Three files: `launch_sc2.sh` (starts the game in remote-control mode),
`run_bot.sh` (runs the bot), `bot.py` (the AI logic — edit this).

## One-time setup on the Mac
1. Install Battle.net + StarCraft II (free-to-play account is fine).
   The client runs under Rosetta 2 on Apple Silicon — normal.
2. Launch SC2 once manually, log in with the account you'll dedicate to bots.
3. In this folder:
   ```bash
   python3 -m venv .venv
   .venv/bin/pip install sc2
   chmod +x launch_sc2.sh run_bot.sh
   ```

## Each session
```bash
SC2_ACCOUNT=you@example.com ./launch_sc2.sh   # wait for main menu
./run_bot.sh                                    # zerg vs terran/easy
./run_bot.sh --race terran --opponent-race zerg --difficulty harder
```
The bot joins/creates a local game on port 5000 and plays automatically.

## Notes / gotchas
- `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python` is set by run_bot.sh —
  required because python-sc2's protobuf stubs predate protobuf 4.
- Map names must exist in your installed SC2 (`--map 2000AtmospheresA` default;
  try `AutomatCity`, `Dreamcatcher`, `Ephemeron`).
- Bot-vs-bot ladder matchmaking is disabled by Blizzard; you play built-in AIs.
- To add an LLM at the strategy layer later: replace `build_army_and_attack()`
  with calls to your model (via openbrouter), keeping harvest/micro in python-sc2.
- If a command fails with "unable to connect", the client isn't in RC mode —
  fully quit SC2 and re-run launch_sc2.sh.
