"""Minimal python-sc2 bot: worker harvest + supply + drones + zergling rush.

Run on the Mac AFTER StarCraft is launched in remote-control mode (see launch_sc2.sh).
Requires PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python (set by run_bot.sh).
"""
import argparse
import asyncio
import math

from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.position import Point2
from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import AIBuild, Difficulty, Race, Result


class MyBot(BotAI):

    async def on_start(self):
        self.enemy_start_locations_known = False

    # ---------- main loop: runs every game step ----------
    async def on_step(self, iteration):
        await self.supply_and_drones()
        await self.harvest_with_idle_workers()
        await self.build_army_and_attack()

    # ---------- economy ----------
    async def supply_and_drones(self):
        workers = self.workers
        # keep overlord/depot supply flowing
        if self.supply_left < 3 and self.can_afford(self.race.supply_depot):
            await self.build(self.race.supply_depot)
        # cap drones at 64
        if len(workers) < 64 and self.supply_left > 0 and self.can_afford(self.race.worker):
            await self.build(self.race.worker)

    async def harvest_with_idle_workers(self):
        for w in self.workers.idle:
            if self.mineral_field:
                w.gather(self.mineral_field.closest_to(w))
            elif self.vespene_geyser:
                w.gather(self.vespene_geyser.closest_to(w))

    # ---------- army ----------
    async def build_army_and_attack(self):
        race = self.race
        # one barracks / hatchery / gateway to start production
        if not self.structures(race.production_structures.first):
            if self.can_afford(race.production_structures.first):
                await self.build(race.production_structures.first,
                                 placement=self.get_next_placement())
            return

        # train combat units up to an army cap
        army = self.units(race.melee_units) + self.units(race.ranged_units)
        if len(army) < 30 and self.supply_left > 2:
            prod = self.structures(race.production_structures.first).ready
            if prod:
                unit_type = race.melee_units or race.ranged_units
                if unit_type and self.can_afford(unit_type):
                    prod.random.train(unit_type)

        # attack wave once we have a small army
        if len(army) >= 20 and not getattr(self, "attacked", False):
            target = self.enemy_structures or None
            dest = (target[0].position if target
                    else self.enemy_start_locations[0])
            for u in army:
                u.attack(dest)
            self.attacked = True

    # ---------- helpers ----------
    def get_next_placement(self):
        """Crude placement: ring outward from the main base until a spot is free."""
        main = self.start_location
        for r in range(5, 40, 3):
            for angle in range(0, 360, 30):
                dx = r * math.cos(math.radians(angle))
                dy = r * math.sin(math.radians(angle))
                p = Point2((main.x + dx, main.y + dy))
                if self.is_position_available(p):
                    return p
        return None


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", default="2000AtmospheresA")
    ap.add_argument("--race", default="zerg", choices=["terran", "zerg", "protoss"])
    ap.add_argument("--opponent-race", default="terran")
    ap.add_argument("--difficulty", default="easy",
                    choices=["very_easy", "easy", "medium", "hard", "harder", "hardest"])
    ap.add_argument("--port", type=int, default=5000)
    return ap.parse_args()


if __name__ == "__main__":
    args = parse_args()
    my_race = Race(args.race.upper())
    opp_race = Race(args.opponent_race.upper())
    difficulty = {"very_easy": Difficulty.veryeasy, "easy": Difficulty.easy,
                  "medium": Difficulty.medium, "hard": Difficulty.hard,
                  "harder": Difficulty.harder, "hardest": Difficulty.hardest}[args.difficulty]

    print(f"[bot] map={args.map} race={args.race} vs {args.opponent_race}"
          f" ({args.difficulty}) port={args.port}")
    run_game(
        maps.get(args.map),
        [Bot(my_race, MyBot()), Computer(opp_race, difficulty)],
        portdata=args.port,
        realtime=False,
    )
