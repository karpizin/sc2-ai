import sc2
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId

class EconomyManager:
    def __init__(self, bot):
        self.bot = bot
        self.max_workers = 80 # Глобальный лимит

    async def update(self):
        await self._manage_workers()
        await self._manage_gas()
        await self._use_chrono_boost()

    async def _manage_workers(self):
        """Строит рабочих, если их не хватает для насыщения текущих баз."""
        for nexus in self.bot.townhalls.ready.idle:
            # Оптимальное количество рабочих = количество баз * 22 (16 на минералы + 6 на 2 газа)
            needed_workers = self.bot.townhalls.amount * 22
            if self.bot.supply_workers < needed_workers and self.bot.supply_workers < self.max_workers:
                if self.bot.can_afford(UnitTypeId.PROBE):
                    nexus.train(UnitTypeId.PROBE)

    async def _manage_gas(self):
        """Строит ассимиляторы на гейзерах рядом с готовыми Нексусами."""
        if self.bot.structures(UnitTypeId.ASSIMILATOR).amount < self.bot.townhalls.ready.amount * 2:
            for nexus in self.bot.townhalls.ready:
                vgs = self.bot.vespene_geyser.closer_than(15, nexus)
                for vg in vgs:
                    if not self.bot.can_afford(UnitTypeId.ASSIMILATOR):
                        break
                    
                    worker = self.bot.select_build_worker(vg.position)
                    if worker and not self.bot.structures(UnitTypeId.ASSIMILATOR).closer_than(1.0, vg).exists:
                        worker.build(UnitTypeId.ASSIMILATOR, vg)

    async def _use_chrono_boost(self):
        """Использует энергию Нексуса для ускорения производства рабочих."""
        if self.bot.townhalls.exists:
            nexus = self.bot.townhalls.ready.random
            if nexus.energy >= 50:
                # Если Нексус что-то строит (рабочего), кидаем буст на него
                if not nexus.is_idle and not nexus.has_buff(sc2.ids.buff_id.BuffId.CHRONOBOOSTENERGYCOST):
                    nexus(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, nexus)
                # Позже добавим логику буста на гейтвеи/апгрейды
