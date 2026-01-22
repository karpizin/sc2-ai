import sc2
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId

class EconomyManager:
    def __init__(self, bot):
        self.bot = bot
        self.max_workers = 80

    async def update(self):
        await self._manage_workers()
        await self._manage_gas_buildings()
        await self._balance_gas_workers()
        await self._use_chrono_boost()
        await self._micro_manage_mining()

    async def _manage_workers(self):
        """Строит рабочих."""
        for nexus in self.bot.townhalls.ready.idle:
            needed_workers = self.bot.townhalls.amount * 22
            if self.bot.supply_workers < needed_workers and self.bot.supply_workers < self.max_workers:
                if self.bot.can_afford(UnitTypeId.PROBE):
                    nexus.train(UnitTypeId.PROBE)

    async def _manage_gas_buildings(self):
        """Строит ассимиляторы."""
        # Строим газ только если есть первый гейтвей или мы в макро
        if not self.bot.structures(UnitTypeId.GATEWAY).exists and not self.bot.structures(UnitTypeId.WARPGATE).exists:
            if self.bot.townhalls.amount == 1:
                return

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

    async def _balance_gas_workers(self):
        """Обеспечивает ровно 3 рабочих на каждый ассимилятор."""
        for assimilator in self.bot.structures(UnitTypeId.ASSIMILATOR).ready:
            # Сколько рабочих сейчас назначено на этот газ
            current_workers = self.bot.workers.filter(lambda w: w.is_gathering and w.orders and w.orders[0].target == assimilator.tag)
            
            # Если рабочих не хватает - берем с минералов
            if current_workers.amount < 3:
                needed = 3 - current_workers.amount
                potential_workers = self.bot.workers.gathering.filter(lambda w: w.is_carrying_minerals or not w.is_carrying_resource)
                if potential_workers.exists:
                    for i in range(min(needed, potential_workers.amount)):
                        worker = potential_workers[i]
                        worker.gather(assimilator)

            # Если рабочих слишком много - отправляем лишних на минералы
            elif current_workers.amount > 3:
                extras = current_workers.amount - 3
                for i in range(extras):
                    worker = current_workers[i]
                    worker.gather(self.bot.mineral_field.closest_to(worker))

    async def _use_chrono_boost(self):
        """Chrono Boost на Нексус."""
        if self.bot.townhalls.exists:
            nexus = self.bot.townhalls.ready.random
            if nexus.energy >= 50:
                if not nexus.is_idle and not nexus.has_buff(sc2.ids.buff_id.BuffId.CHRONOBOOSTENERGYCOST):
                    nexus(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, nexus)

    async def _micro_manage_mining(self):
        """Ускоренный майнинг (Mineral Micro)."""
        # Мы применяем микро только для тех, кто не на газу
        mining_workers = self.bot.workers.filter(lambda w: w.is_gathering or w.is_returning)
        
        for worker in mining_workers:
            if not worker.orders:
                continue
                
            target_tag = worker.orders[0].target
            target_obj = self.bot.structures(UnitTypeId.ASSIMILATOR).find_by_tag(target_tag)
            
            # Если рабочий идет на ГАЗ - не мешаем ему стандартной логикой (там микро сложнее)
            if target_obj:
                continue

            # Логика для МИНЕРАЛОВ
            if worker.is_returning:
                target = self.bot.townhalls.closest_to(worker)
                if worker.distance_to(target) > 2.8:
                    worker.move(target.position)
                else:
                    worker.return_resource()
            elif worker.is_gathering:
                target = self.bot.mineral_field.find_by_tag(target_tag)
                if target and worker.distance_to(target) > 1.5:
                    worker.move(target.position)
                else:
                    worker.gather(target)
