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
        strategy = self.bot.intel_manager.get_enemy_info()["strategy"]
        is_threatened = strategy in {"PROXY_DETECTED", "CONFIRMED_PROXY", "CHEESE_ALL_IN"}

        # Повышаем порог атаки, если мы под угрозой
        effective_threshold = self.attack_threshold + (10 if is_threatened else 0)
        
        # Если есть прямая угроза - ВСЯ армия защищает базу
        if is_threatened:
            enemy_near_base = self.bot.enemy_units.closer_than(30, self.bot.townhalls.first)
            if enemy_near_base.exists:
                target = enemy_near_base.closest_to(self.bot.townhalls.first)
                for unit in army.idle:
                    unit.attack(target)
                return
            else:
                # Ждем врага на рампе
                rally_point = self.bot.main_base_ramp.top_center
                for unit in army.idle:
                    unit.move(rally_point)
                return

        # Обычная логика атаки
        if army.amount >= effective_threshold:
            enemy_pos = self.bot.intel_manager.get_enemy_info()["main_pos"]
            if enemy_pos:
                for unit in army.idle:
                    unit.attack(enemy_pos)
