import sc2
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId

class ProductionManager:
    def __init__(self, bot):
        self.bot = bot

    async def update(self):
        await self._manage_supply()
        await self._build_infrastructure()
        await self._research_upgrades()

    async def _manage_supply(self):
        """Строит пилоны, если лимит заканчивается."""
        if self.bot.supply_left < 5 and self.bot.supply_cap < 200:
            if self.bot.already_pending(UnitTypeId.PYLON) == 0:
                if self.bot.can_afford(UnitTypeId.PYLON):
                    # Строим рядом с Нексусом
                    if self.bot.townhalls.ready.exists:
                        await self.bot.build(UnitTypeId.PYLON, near=self.bot.townhalls.ready.random)

    async def _build_infrastructure(self):
        """Адаптивная постройка зданий."""
        if not self.bot.townhalls.ready.exists:
            return

        nexus = self.bot.townhalls.ready.random

        # 1. Пилон должен быть всегда первым
        if self.bot.structures(UnitTypeId.PYLON).amount == 0 and self.bot.already_pending(UnitTypeId.PYLON) == 0:
            if self.bot.can_afford(UnitTypeId.PYLON):
                await self.bot.build(UnitTypeId.PYLON, near=nexus)
            return

        # Находим готовый пилон для застройки рядом
        pylons = self.bot.structures(UnitTypeId.PYLON).ready
        if not pylons.exists:
            return
        pylon = pylons.random

        # 2. Gateway (первый)
        if self.bot.structures(UnitTypeId.GATEWAY).amount + self.bot.structures(UnitTypeId.WARPGATE).amount == 0:
            if self.bot.already_pending(UnitTypeId.GATEWAY) == 0:
                if self.bot.can_afford(UnitTypeId.GATEWAY):
                    await self.bot.build(UnitTypeId.GATEWAY, near=pylon)

        # 3. Cybernetics Core (как только готов первый Gateway)
        elif self.bot.structures(UnitTypeId.GATEWAY).ready.exists and self.bot.structures(UnitTypeId.CYBERNETICSCORE).amount == 0:
            if self.bot.already_pending(UnitTypeId.CYBERNETICSCORE) == 0:
                if self.bot.can_afford(UnitTypeId.CYBERNETICSCORE):
                    await self.bot.build(UnitTypeId.CYBERNETICSCORE, near=pylon)

        # 4. Дополнительные Gateways (адаптивно: если много минералов — строим больше)
        else:
            # Держим минимум 4 гейтвея на одну базу
            max_gateways = self.bot.townhalls.amount * 4
            current_gateways = self.bot.structures(UnitTypeId.GATEWAY).amount + self.bot.structures(UnitTypeId.WARPGATE).amount
            
            if current_gateways < max_gateways and self.bot.can_afford(UnitTypeId.GATEWAY):
                if self.bot.already_pending(UnitTypeId.GATEWAY) < 1:
                    await self.bot.build(UnitTypeId.GATEWAY, near=pylon)

    async def _research_upgrades(self):
        """Исследования (в первую очередь Warp Gate)."""
        if self.bot.structures(UnitTypeId.CYBERNETICSCORE).ready.idle.exists:
            core = self.bot.structures(UnitTypeId.CYBERNETICSCORE).ready.idle.first
            if self.bot.can_afford(UpgradeId.WARPGATERESEARCH) and not self.bot.already_pending_upgrade(UpgradeId.WARPGATERESEARCH):
                core.research(UpgradeId.WARPGATERESEARCH)
