import sc2
from sc2.ids.unit_typeid import UnitTypeId

class ScoutManager:
    def __init__(self, bot):
        self.bot = bot
        self.scout_tag = None # ID рабочего-разведчика
        self.started_scouting = False

    async def update(self):
        await self._manage_scout()

    async def _manage_scout(self):
        # 1. Отправляем разведку, когда лимит > 13
        if not self.started_scouting and self.bot.supply_used >= 13:
            worker = self.bot.workers.gathering.random
            if worker:
                self.scout_tag = worker.tag
                self.started_scouting = True
                # Едем на стартовую позицию врага
                worker.move(self.bot.enemy_start_locations[0])

        # 2. Логика поведения разведчика
        if self.scout_tag:
            scout = self.bot.workers.find_by_tag(self.scout_tag)
            
            # Если разведчик погиб, пробуем отправить нового позже (если еще начало игры)
            if not scout:
                self.scout_tag = None
                return

            enemy_base = self.bot.enemy_start_locations[0]
            
            # Если мы доехали до базы врага, начинаем "кружить" вокруг зданий
            if scout.distance_to(enemy_base) < 20:
                # Если видим вражеских юнитов (не рабочих), держим дистанцию
                threats = self.bot.enemy_units.filter(lambda u: u.type_id not in {UnitTypeId.PROBE, UnitTypeId.SCV, UnitTypeId.DRONE})
                if threats.exists:
                    closest_threat = threats.closest_to(scout)
                    if closest_threat.distance_to(scout) < 5:
                        # Убегаем к своей базе
                        scout.move(self.bot.townhalls.first.position)
                else:
                    # Если угроз нет, просто "патрулируем" базу врага, чтобы IntelManager видел здания
                    if scout.is_idle:
                        # Берем случайную позицию в радиусе базы
                        target = enemy_base.random_on_distance(10)
                        scout.move(target)
            
            # Если разведчик серьезно ранен, отправляем домой
            if scout.health_percentage < 0.5:
                scout.move(self.bot.townhalls.first.position)
                # Когда вернется, пусть добывает минералы (освобождаем роль разведчика)
                if scout.distance_to(self.bot.townhalls.first) < 5:
                    scout.gather(self.bot.mineral_field.closest_to(scout))
                    self.scout_tag = None
