import sc2
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2

class IntelManager:
    def __init__(self, bot):
        self.bot = bot
        # Память о зданиях врага: {unit_id: {'type': UnitTypeId, 'pos': Point2}}
        self.enemy_structures_memory = {}
        self.enemy_workers_count = 0
        self.enemy_main_base_location = None
        self.inferred_strategy = "UNKNOWN" # MACRO, RUSH, ALL_IN, TECH

    async def update(self):
        self._update_enemy_memory()
        self._count_enemy_workers()
        self._guess_enemy_main()
        self._analyze_strategy()

    def _update_enemy_memory(self):
        """Обновляет информацию о зданиях врага."""
        for structure in self.bot.enemy_structures:
            self.enemy_structures_memory[structure.id] = {
                "type": structure.type_id,
                "pos": structure.position,
                "last_seen": self.bot.time
            }
        
        to_delete = []
        for unit_id, data in self.enemy_structures_memory.items():
            if self.bot.is_visible(data["pos"]):
                if not any(s.id == unit_id for s in self.bot.enemy_structures):
                    to_delete.append(unit_id)
        
        for unit_id in to_delete:
            del self.enemy_structures_memory[unit_id]

    def _count_enemy_workers(self):
        """Считает видимых рабочих врага."""
        workers = self.bot.enemy_units.filter(lambda u: u.type_id in {UnitTypeId.PROBE, UnitTypeId.SCV, UnitTypeId.DRONE})
        self.enemy_workers_count = max(self.enemy_workers_count, workers.amount)

    def _analyze_strategy(self):
        """Анализирует стратегию оппонента на основе увиденного."""
        game_time = self.bot.time # время в секундах
        
        # 1. Детекция RUSH (мало рабочих на раннем этапе + агрессивные здания)
        if game_time < 180: # первые 3 минуты
            # Если мы увидели базу врага, но там подозрительно мало рабочих
            if self.enemy_main_base_location and self.bot.is_visible(self.enemy_main_base_location):
                if self.enemy_workers_count > 0 and self.enemy_workers_count < 12:
                    self.inferred_strategy = "RUSH"
            
            # Проверка на прокси-здания или ранние пулы
            for data in self.enemy_structures_memory.values():
                if data["type"] == UnitTypeId.BARRACKS and data["pos"].distance_to(self.enemy_main_base_location) > 50:
                    self.inferred_strategy = "PROXY_RUSH"
                if data["type"] == UnitTypeId.SPAWNINGPOOL and game_time < 100:
                    self.inferred_strategy = "EARLY_POOL"

        # 2. Детекция макро (быстрая вторая база)
        townhalls = [d for d in self.enemy_structures_memory.values() if d["type"] in {UnitTypeId.NEXUS, UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY}]
        if len(townhalls) >= 2 and game_time < 240:
            self.inferred_strategy = "MACRO"

    def get_enemy_info(self):
        return {
            "structures": self.enemy_structures_memory,
            "main_pos": self.enemy_main_base_location,
            "workers": self.enemy_workers_count,
            "strategy": self.inferred_strategy
        }
