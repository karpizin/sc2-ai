import sc2
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.units import Units

class EconomyManager:
    def __init__(self, bot):
        self.bot = bot
        self.max_workers = 80

    async def update(self):
        await self._manage_workers()
        await self._manage_gas()
        await self._use_chrono_boost()
        await self._micro_manage_mining()

    async def _manage_workers(self):
        """Строит рабочих."""
        for nexus in self.bot.townhalls.ready.idle:
            needed_workers = self.bot.townhalls.amount * 22
            if self.bot.supply_workers < needed_workers and self.bot.supply_workers < self.max_workers:
                if self.bot.can_afford(UnitTypeId.PROBE):
                    nexus.train(UnitTypeId.PROBE)

    async def _manage_gas(self):
        """Строит ассимиляторы."""
        if self.bot.structures(UnitTypeId.ASSIMILATOR).amount < self.bot.townhalls.ready.amount * 2:
            for nexus in self.bot.townhalls.ready:
                vgs = self.bot.vespene_geyser.closer_than(15, nexus)
                for vg in vgs:
                    if not self.bot.can_afford(UnitTypeId.ASSIMILATOR):
                        break
                    if not self.bot.structures(UnitTypeId.ASSIMILATOR).closer_than(1.0, vg).exists:
                        worker = self.bot.select_build_worker(vg.position)
                        if worker:
                            worker.build(UnitTypeId.ASSIMILATOR, vg)

    async def _use_chrono_boost(self):
        """Chrono Boost на Нексус."""
        if self.bot.townhalls.exists:
            nexus = self.bot.townhalls.ready.random
            if nexus.energy >= 50:
                if not nexus.is_idle and not nexus.has_buff(sc2.ids.buff_id.BuffId.CHRONOBOOSTENERGYCOST):
                    nexus(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, nexus)

    async def _micro_manage_mining(self):
        """
        Ускоренный майнинг (Mineral Micro).
        Убирает фазу торможения рабочих перед минералами и ратушей.
        """
        for worker in self.bot.workers.filter(lambda w: w.is_gathering or w.is_returning):
            target = None
            
            # Если рабочий несет минералы - его цель Нексус
            if worker.is_returning:
                target = self.bot.townhalls.closest_to(worker)
                distance_threshold = 2.8 # Дистанция до Нексуса, когда нужно переключить на сдачу
                
                # Если мы еще далеко, используем move вместо return_resource, чтобы не тормозить
                if worker.distance_to(target) > distance_threshold:
                    worker.move(target.position)
                else:
                    worker.return_resource()

            # Если рабочий пустой - его цель минералы
            elif worker.is_gathering:
                # Находим минерал, к которому он прикреплен
                # В python-sc2 orders[0].target дает ID объекта
                if worker.orders:
                    target_id = worker.orders[0].target
                    # Пытаемся найти этот минерал среди всех минералов на карте
                    target = self.bot.mineral_field.find_by_tag(target_id)
                
                if target:
                    distance_threshold = 1.5 # Дистанция до минерала
                    if worker.distance_to(target) > distance_threshold:
                        worker.move(target.position)
                    else:
                        worker.gather(target)