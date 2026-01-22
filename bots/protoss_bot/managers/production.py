import sc2
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId

class ProductionManager:
    def __init__(self, bot):
        self.bot = bot

    async def update(self):
        await self._manage_supply()
        await self._manage_expansions()
        await self._build_infrastructure()
        await self._research_upgrades()
        await self._base_defense()

    async def _manage_supply(self):
        """Строит пилоны."""
        # Увеличиваем порог supply_left в зависимости от количества баз
        threshold = 5 + (self.bot.townhalls.amount * 2)
        if self.bot.supply_left < threshold and self.bot.supply_cap < 200:
            if self.bot.already_pending(UnitTypeId.PYLON) < self.bot.townhalls.amount:
                if self.bot.can_afford(UnitTypeId.PYLON):
                    if self.bot.townhalls.ready.exists:
                        await self.bot.build(UnitTypeId.PYLON, near=self.bot.townhalls.ready.random)

    async def _manage_expansions(self):
        """Логика расширения на новые базы."""
        # 1. Если мы уже строим базу - ждем
        if self.bot.already_pending(UnitTypeId.NEXUS):
            return

        # 2. Условия для экспансии:
        # - Много минералов (> 400)
        # - Или текущие базы почти забиты рабочими
        should_expand = False
        if self.bot.can_afford(UnitTypeId.NEXUS):
            if self.bot.minerals > 800: # Избыток ресурсов
                should_expand = True
            elif self.bot.supply_workers > (self.bot.townhalls.amount * 18): # Насыщение близко
                should_expand = True

        if should_expand:
            # Находим ближайшее свободное место для экспансии
            await self.bot.expand_now()

    async def _build_infrastructure(self):
        """Постройка зданий (Gateway, CyberCore, etc)."""
        if not self.bot.townhalls.ready.exists:
            return

        nexus = self.bot.townhalls.ready.random
        pylons = self.bot.structures(UnitTypeId.PYLON).ready
        
        if not pylons.exists:
            if self.bot.can_afford(UnitTypeId.PYLON) and not self.bot.already_pending(UnitTypeId.PYLON):
                await self.bot.build(UnitTypeId.PYLON, near=nexus)
            return

        pylon = pylons.random
        strategy = self.bot.intel_manager.get_enemy_info()["strategy"]
        is_threatened = strategy in {"PROXY_DETECTED", "CONFIRMED_PROXY", "CHEESE_ALL_IN"}

        # Базовая технологическая цепочка
        if self.bot.structures(UnitTypeId.GATEWAY).amount + self.bot.structures(UnitTypeId.WARPGATE).amount == 0:
            if self.bot.already_pending(UnitTypeId.GATEWAY) == 0:
                if self.bot.can_afford(UnitTypeId.GATEWAY):
                    await self.bot.build(UnitTypeId.GATEWAY, near=pylon)

        elif self.bot.structures(UnitTypeId.GATEWAY).ready.exists and self.bot.structures(UnitTypeId.CYBERNETICSCORE).amount == 0:
            if self.bot.already_pending(UnitTypeId.CYBERNETICSCORE) == 0:
                if self.bot.can_afford(UnitTypeId.CYBERNETICSCORE):
                    await self.bot.build(UnitTypeId.CYBERNETICSCORE, near=pylon)
        
        # ЭКСТРЕННЫЙ FORGE: если угроза, строим даже на одной базе
        elif is_threatened and self.bot.structures(UnitTypeId.FORGE).amount == 0:
            if self.bot.already_pending(UnitTypeId.FORGE) == 0:
                if self.bot.can_afford(UnitTypeId.FORGE):
                    await self.bot.build(UnitTypeId.FORGE, near=pylon)

        # Forge для пушек (нормальный режим - если больше 1 базы)
        elif self.bot.townhalls.amount > 1 and self.bot.structures(UnitTypeId.FORGE).amount == 0:
            if self.bot.already_pending(UnitTypeId.FORGE) == 0:
                if self.bot.can_afford(UnitTypeId.FORGE):
                    await self.bot.build(UnitTypeId.FORGE, near=pylon)

        # Масштабирование Gateway
        else:
            max_gateways = self.bot.townhalls.amount * 3
            current_gateways = self.bot.structures(UnitTypeId.GATEWAY).amount + self.bot.structures(UnitTypeId.WARPGATE).amount
            
            if current_gateways < max_gateways and self.bot.can_afford(UnitTypeId.GATEWAY):
                if self.bot.already_pending(UnitTypeId.GATEWAY) < 1:
                    await self.bot.build(UnitTypeId.GATEWAY, near=pylon)

    async def _base_defense(self):
        """Минимальная защита баз."""
        strategy = self.bot.intel_manager.get_enemy_info()["strategy"]
        is_threatened = strategy in {"PROXY_DETECTED", "CONFIRMED_PROXY", "CHEESE_ALL_IN"}

        if self.bot.structures(UnitTypeId.FORGE).ready.exists:
            for nexus in self.bot.townhalls.ready:
                # В случае угрозы строим больше защиты (2 пушки + 2 батарейки)
                num_needed = 2 if is_threatened else 1
                
                # Фотонки
                if self.bot.structures(UnitTypeId.PHOTONCANNON).closer_than(10, nexus).amount < num_needed:
                    if self.bot.can_afford(UnitTypeId.PHOTONCANNON):
                        pylons = self.bot.structures(UnitTypeId.PYLON).ready.closer_than(10, nexus)
                        if pylons.exists:
                            await self.bot.build(UnitTypeId.PHOTONCANNON, near=pylons.random)

                # Батарейки
                if self.bot.structures(UnitTypeId.CYBERNETICSCORE).ready.exists:
                    if self.bot.structures(UnitTypeId.SHIELDBATTERY).closer_than(10, nexus).amount < num_needed:
                        if self.bot.can_afford(UnitTypeId.SHIELDBATTERY):
                            pylons = self.bot.structures(UnitTypeId.PYLON).ready.closer_than(10, nexus)
                            if pylons.exists:
                                await self.bot.build(UnitTypeId.SHIELDBATTERY, near=pylons.random)

    async def _research_upgrades(self):
        """Исследования."""
        if self.bot.structures(UnitTypeId.CYBERNETICSCORE).ready.idle.exists:
            core = self.bot.structures(UnitTypeId.CYBERNETICSCORE).ready.idle.first
            if self.bot.can_afford(UpgradeId.WARPGATERESEARCH) and not self.bot.already_pending_upgrade(UpgradeId.WARPGATERESEARCH):
                core.research(UpgradeId.WARPGATERESEARCH)
