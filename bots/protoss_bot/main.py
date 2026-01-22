import sc2
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.ids.unit_typeid import UnitTypeId

from managers.intel import IntelManager
from managers.economy import EconomyManager
from managers.production import ProductionManager
from managers.army import ArmyManager
from managers.scout import ScoutManager

class ProtossModularBot(sc2.BotAI):
    def __init__(self):
        super().__init__()
        self.intel_manager = IntelManager(self)
        self.economy_manager = EconomyManager(self)
        self.production_manager = ProductionManager(self)
        self.army_manager = ArmyManager(self)
        self.scout_manager = ScoutManager(self)

    async def on_step(self, iteration: int):
        # 1. Обновляем информацию (Intel)
        await self.intel_manager.update()

        # 2. Выполняем действия
        # Стандартный distribute_workers отключен для работы Mineral Micro в economy_manager
        # await self.distribute_workers()
        await self.economy_manager.update()
        await self.production_manager.update()
        await self.army_manager.update()
        await self.scout_manager.update()
        await self._debug_info()

    async def _debug_info(self):
        """Выводит отладочную информацию на экран."""
        enemy_info = self.intel_manager.get_enemy_info()
        num_structures = len(enemy_info["structures"])
        strategy = enemy_info["strategy"]
        workers = enemy_info["workers"]

        # Текст на экране
        self.client.debug_text_screen(f"Inferred Strategy: {strategy}", (0.01, 0.1), color=(255, 255, 0), size=14)
        self.client.debug_text_screen(f"Enemy Workers Seen: {workers}", (0.01, 0.13), color=(255, 255, 0), size=14)
        self.client.debug_text_screen(f"Enemy structures in memory: {num_structures}", (0.01, 0.16), color=(0, 255, 0), size=12)
        
        for data in enemy_info["structures"].values():
            self.client.debug_sphere_out(data["pos"], 1.0, color=(0, 255, 0))

def main():
    run_game(
        sc2.maps.get("AcropolisAI"),
        [Bot(sc2.Race.Protoss, ProtossModularBot()), Computer(sc2.Race.Zerg, sc2.Difficulty.Easy)],
        realtime=False,
    )

if __name__ == "__main__":
    main()
