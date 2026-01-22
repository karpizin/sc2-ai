import sc2
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2

class IntelManager:
    def __init__(self, bot):
        self.bot = bot
        # Память о зданиях врага: {unit_id: {'type': UnitTypeId, 'pos': Point2}}
        self.enemy_structures_memory = {}
        self.enemy_main_base_location = None

    async def update(self):
        self._update_enemy_memory()
        self._guess_enemy_main()

    def _update_enemy_memory(self):
        """Обновляет информацию о зданиях врага, которые мы видим сейчас."""
        for structure in self.bot.enemy_structures:
            self.enemy_structures_memory[structure.id] = {
                "type": structure.type_id,
                "pos": structure.position,
                "last_seen": self.bot.time
            }
        
        # Удаляем из памяти здания, если мы видим их местоположение, но их там нет
        to_delete = []
        for unit_id, data in self.enemy_structures_memory.items():
            if self.bot.is_visible(data["pos"]):
                # Если место видно, но нашего юнита с таким ID там нет (среди видимых врагов)
                if not any(s.id == unit_id for s in self.bot.enemy_structures):
                    to_delete.append(unit_id)
        
        for unit_id in to_delete:
            del self.enemy_structures_memory[unit_id]

    def _guess_enemy_main(self):
        """Пытаемся определить, где главная база."""
        if not self.enemy_main_base_location:
            if self.bot.enemy_start_locations:
                self.enemy_main_base_location = self.bot.enemy_start_locations[0]
            # Если увидели ратушу в другом месте, обновляем
            for data in self.enemy_structures_memory.values():
                if data["type"] in {UnitTypeId.NEXUS, UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY}:
                    self.enemy_main_base_location = data["pos"]

    def get_enemy_info(self):
        return {
            "structures": self.enemy_structures_memory,
            "main_pos": self.enemy_main_base_location
        }
