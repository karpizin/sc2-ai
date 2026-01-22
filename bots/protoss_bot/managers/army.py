import sc2
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId

class ArmyManager:
    def __init__(self, bot):
        self.bot = bot
        self.attack_threshold = 15 # Минимум юнитов для начала атаки

    async def update(self):
        await self._manage_production()
        await self._manage_warpgates()
        await self._execute_attack()

    async def _manage_production(self):
        """Нанимает юнитов через обычные Gateway (пока не готов Warp Gate)."""
        gateways = self.bot.structures(UnitTypeId.GATEWAY).ready.idle
        for gateway in gateways:
            # Приоритет Сталкерам, если есть кибернетка
            if self.bot.structures(UnitTypeId.CYBERNETICSCORE).ready.exists:
                if self.bot.can_afford(UnitTypeId.STALKER) and self.bot.supply_left > 0:
                    gateway.train(UnitTypeId.STALKER)
            # Иначе Адепты или Зилоты
            elif self.bot.can_afford(UnitTypeId.ADEPT) and self.bot.supply_left > 0:
                gateway.train(UnitTypeId.ADEPT)

    async def _manage_warpgates(self):
        """Трансформирует Gateway в Warp Gate."""
        for gateway in self.bot.structures(UnitTypeId.GATEWAY).ready.idle:
            if self.bot.can_afford(AbilityId.MORPH_WARPGATE):
                gateway(AbilityId.MORPH_WARPGATE)

    async def _execute_attack(self):
        """Логика атаки: если армия большая — идем к врагу."""
        army = self.bot.units.filter(lambda u: u.type_id in {UnitTypeId.ZEALOT, UnitTypeId.STALKER, UnitTypeId.ADEPT})
        
        if army.amount >= self.attack_threshold:
            enemy_pos = self.bot.intel_manager.get_enemy_info()["main_pos"]
            if enemy_pos:
                for unit in army.idle:
                    unit.attack(enemy_pos)
        
        # Если армии мало, собираем её у входа на базу (Natural)
        else:
            if self.bot.townhalls.exists:
                rally_point = self.bot.main_base_ramp.top_center
                for unit in army.idle:
                    unit.move(rally_point)
