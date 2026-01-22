# StarCraft II AI Resources & Ecosystem

Ниже — «затравка» коллекции GitHub‑репозиториев по StarCraft II, с упором на API, фреймворки, шаблоны ботов и инфраструктуру турниров.

---

## 🛠 Официальный API и протокол

- **s2client-api** (C++, офиц. клиент): [github](https://github.com/Blizzard/s2client-api)
- **SC2API документация** (GitHub Pages): [blizzard.github](https://blizzard.github.io/s2client-api/)
- **s2client-proto** (protobuf‑описания протокола): [github](https://github.com/Blizzard/s2client-proto)

## 🐍 Python‑стек и фреймворки

- **python-sc2** (fork BurnySc2, де‑факто стандарт): [github](https://github.com/BurnySc2/python-sc2)
- **python-sc2** (оригинальный Dentosal): [github](https://github.com/Dentosal/python-sc2)
- **Ares SC2 фреймворк**: [aressc2.github](https://aressc2.github.io/ares-sc2/)
- **Ares SC2 bot template** (шаблон бота + CI + авто‑аплоад в AI Arena): [github](https://github.com/AresSC2/ares-sc2-bot-template)

## 🤖 Шаблоны ботов и учебные репо

- **ExampleBot** (C# пример бота): [github](https://github.com/SimonPrins/ExampleBot)
- **VersusAI SC2 bot template** (Python): [versusai](https://versusai.net/labs/simple-starcraft-2-bot-template-to-get-started-in-python/)
- **StarCraft.AI Tutorials**: Примеры ботов (cannon rush, worker rush и др.) [starcraft](https://starcraft.ai/blog/creating-starcraft-bots-in-python)
- **Individual bot-repository**: Пример структуры реального проекта [github](https://github.com/tsmerda/starcraft-bot)

## 🏆 Турниры, локальный лаунчер и AI Arena

- **AI Arena local-play-bootstrap**: Локальный запуск матчей в docker [github](https://github.com/aiarena/local-play-bootstrap)
- **AI Arena Wiki (Bot Development)**: Ссылки на скачиваемые боты и исходники [aiarena](https://aiarena.net/wiki/bot-development/_source/)

## 🔍 Каталоги и дальнейший поиск

- **GitHub topic starcraft2**: Общий список репозиториев [github](https://github.com/topics/starcraft2)
- **python-sc2 Dependents**: Список проектов, использующих библиотеку [github](https://github.com/BurnySc2/python-sc2/network/dependents)

---

## 🐍 Глубокое погружение в Python-экосистему

С учётом того, что разработка ведется на Python, ниже — отфильтрованный список репозиториев и ресурсов вокруг этого стека.

### Библиотеки и фреймворки (Python)

- **python-sc2 (BurnySc2 fork)** — актуальная Python‑обёртка над SC2 API, с кучей примеров (worker rush, cannon rush и т.п.): [github](https://github.com/BurnySc2/python-sc2)
- **python-sc2 (оригинальный Dentosal)** — исходная версия библиотеки, от которой форкнулся Burny, тоже с примерами ботов: [github](https://github.com/Dentosal/python-sc2)
- **Ares SC2** — расширенный фреймворк поверх python‑sc2 (поведение, менеджеры, оптимизированные функции): [github](https://github.com/AresSC2/ares-sc2)

### Шаблоны и стартовые проекты (Python)

- **Ares SC2 bot template** — пустой шаблон бота на базе Ares (готовый run.py, структура, интеграция с AI Arena): [github](https://github.com/AresSC2/ares-sc2-bot-template)
- **VersusAI SC2 bot template** — простой Python‑шаблон с использованием python‑sc2/ares‑sc2: [versusai](https://versusai.net/labs/simple-starcraft-2-bot-template-to-get-started-in-python/)
- **Учебные боты на python-sc2** — в статье StarCraft.AI разбираются Python‑боты (cannon rush и др.) с исходниками на GitHub: [starcraft](https://starcraft.ai/blog/creating-starcraft-bots-in-python)

### Примеры конкретных Python‑ботов и подборки

- **Getting Started Guide**: Пошаговый онбординг для новичков: [GETTING_STARTED.md](GETTING_STARTED.md)
- **BraxBot (Worker Rush)** — пример на python‑sc2 с полным кодом бота на Python: [brax](https://brax.gg/python-sc2-rule-based-bot/)
- **GitHub topic starcraft2-ai (Python)** — отфильтрованный поиск по живым проектам: [github](https://github.com/topics/starcraft2-ai?l=python)
- **ML Bots Overview**: Подробный разбор ML-подходов и проектов: [ML_BOTS_OVERVIEW.md](ML_BOTS_OVERVIEW.md)
- **ML Training Cases**: Репозитории с описанием архитектур и пайплайнов обучения: [ML_TRAINING_CASES.md](ML_TRAINING_CASES.md)
- **awesome-sc2-ai** — curated‑список библиотек, ботов и ресурсов по SC2, в том числе Python‑репо: [github](https://github.com/aiarena/awesome-sc2-ai)

---
*Если хочешь «максимум», следующий шаг — пройтись по awesome‑списку и topic `starcraft2-ai?l=python`, вытащить оттуда только реально живые/боевые Python‑боты и оформить свой curated‑реестр (с указанием расы/стиля/рейтинга на AI Arena).*
