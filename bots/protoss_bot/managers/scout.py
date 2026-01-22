import sc2
from sc2.ids.unit_typeid import UnitTypeId

class ScoutManager:
    def __init__(self, bot):
        self.bot = bot
        self.scout_tag = None 
        self.started_scouting = False
        self.proxy_searcher_tags = set() # Теги юнитов, ищущих прокси
        self.proxy_search_locations = [] # Точки, которые нужно проверить

    async def update(self):
        await self._manage_scout()
        await self._manage_proxy_search()

    async def _manage_scout(self):
        # ... (существующая логика начальной разведки)
        if not self.started_scouting and self.bot.supply_used >= 13:
            worker = self.bot.workers.gathering.random
            if worker:
                self.scout_tag = worker.tag
                self.started_scouting = True
                worker.move(self.bot.enemy_start_locations[0])

        if self.scout_tag:
            scout = self.bot.workers.find_by_tag(self.scout_tag)
            if not scout:
                self.scout_tag = None
                return
            # ... (логика выживания разведчика)
            enemy_base = self.bot.enemy_start_locations[0]
            if scout.distance_to(enemy_base) < 20:
                threats = self.bot.enemy_units.filter(lambda u: u.type_id not in {UnitTypeId.PROBE, UnitTypeId.SCV, UnitTypeId.DRONE})
                if threats.exists:
                    if threats.closest_to(scout).distance_to(scout) < 5:
                        scout.move(self.bot.townhalls.first.position)
                elif scout.is_idle:
                    scout.move(enemy_base.random_on_distance(10))

    async def _manage_proxy_search(self):
        """Логика поиска прокси-зданий вокруг нашей базы."""
        strategy = self.bot.intel_manager.get_enemy_info()["strategy"]
        
        # Если прокси заподозрена, но еще не найдена (не CONFIRMED)
        if strategy == "PROXY_DETECTED":
            # 1. Генерируем точки для поиска (ближайшие экспанды)
            if not self.proxy_search_locations:
                # Берем все точки под базы, сортируем по близости к нам, берем первые 5
                all_expansions = sorted(self.bot.expansion_locations_list, key=lambda p: p.distance_to(self.bot.start_location))
                self.proxy_search_locations = all_expansions[1:6] # Пропускаем мейн, берем натурал и окрестности

            # 2. Набираем поисковый отряд (до 3 юнитов)
            active_searchers = self.bot.units.filter(lambda u: u.tag in self.proxy_searcher_tags)
            
            if active_searchers.amount < 3:
                # Сначала пытаемся взять боевых (Зилоты/Адепты)
                potential_army = self.bot.units.filter(lambda u: u.type_id in {UnitTypeId.ZEALOT, UnitTypeId.ADEPT, UnitTypeId.STALKER} and u.tag not in self.proxy_searcher_tags)
                if potential_army.exists:
                    unit = potential_army.random
                    self.proxy_searcher_tags.add(unit.tag)
                else:
                    # Если армии нет, берем рабочих
                    potential_workers = self.bot.workers.gathering.filter(lambda w: w.tag not in self.proxy_searcher_tags and w.tag != self.scout_tag)
                    if potential_workers.exists:
                        unit = potential_workers.random
                        self.proxy_searcher_tags.add(unit.tag)

            # 3. Рассылаем юнитов по точкам
            for i, unit in enumerate(active_searchers):
                if unit.is_idle and self.proxy_search_locations:
                    # Даем каждому свою точку (циклически)
                    target = self.proxy_search_locations[i % len(self.proxy_search_locations)]
                    unit.move(target)
        
        # Если прокси найдена или угроза миновала - распускаем отряд
        elif strategy == "CONFIRMED_PROXY" or strategy == "MACRO":
            if self.proxy_searcher_tags:
                searchers = self.bot.units.filter(lambda u: u.tag in self.proxy_searcher_tags)
                for unit in searchers:
                    if unit.type_id in {UnitTypeId.PROBE, UnitTypeId.SCV, UnitTypeId.DRONE}:
                        unit.gather(self.bot.mineral_field.closest_to(unit))
                self.proxy_searcher_tags.clear()
                self.proxy_search_locations = []
