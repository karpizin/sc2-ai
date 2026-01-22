import sc2
from sc2 import maps
from sc2.container import Step
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId

class HelloWorldBot(sc2.BotAI):
    async def on_step(self, iteration: int):
        # 1. Distribute workers (standard SC2 efficiency)
        await self.distribute_workers()

        # 2. Build Probes (Workers) up to 22 (optimal for 1 base)
        if self.townhalls:
            nexus = self.townhalls.random
            if self.can_afford(UnitTypeId.PROBE) and nexus.is_idle and self.supply_workers < 22:
                nexus.train(UnitTypeId.PROBE)

        # 3. Build Pylons (Supply) if nearly capped
        if self.supply_left < 4 and self.already_pending(UnitTypeId.PYLON) == 0:
            if self.can_afford(UnitTypeId.PYLON):
                await self.build(UnitTypeId.PYLON, near=nexus)

        # 4. Build Gateways (Production)
        if self.structures(UnitTypeId.PYLON).ready:
            pylon = self.structures(UnitTypeId.PYLON).ready.random
            if self.structures(UnitTypeId.GATEWAY).amount < 3:
                if self.can_afford(UnitTypeId.GATEWAY):
                    await self.build(UnitTypeId.GATEWAY, near=pylon)

        # 5. Build Zealots (Army)
        for gateway in self.structures(UnitTypeId.GATEWAY).ready.idle:
            if self.can_afford(UnitTypeId.ZEALOT) and self.supply_left > 0:
                gateway.train(UnitTypeId.ZEALOT)

        # 6. Attack logic
        # If we have more than 10 zealots, find enemy and attack
        if self.units(UnitTypeId.ZEALOT).amount > 10:
            for zealot in self.units(UnitTypeId.ZEALOT).idle:
                zealot.attack(self.enemy_start_locations[0])

def main():
    run_game(
        maps.get("AcropolisAI"),
        [Bot(sc2.Race.Protoss, HelloWorldBot()), Computer(sc2.Race.Zerg, sc2.Difficulty.Easy)],
        realtime=False,
    )

if __name__ == "__main__":
    main()
