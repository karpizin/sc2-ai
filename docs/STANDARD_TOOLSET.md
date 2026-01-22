# Standard Toolset: SC2 AI Frameworks & Libraries

Для современных ботов в SC2 сформировался довольно устойчивый «набор стандартных» библиотек и фреймворков; ядро в основном одно и то же, вокруг него — надстройки под разные языки.

---

## 🐍 Python

- **python-sc2** — самый распространённый и рекомендуемый интерфейс (AI Arena: «most popular/supported»). Подходит и для скриптовых, и для ML‑ботов. [github](https://github.com/BurnySc2/python-sc2)
- **ares-sc2** — надстройка над python‑sc2 с кучей вспомогательных менеджеров и утилит для макро/микро. [aressc2.github](https://aressc2.github.io/ares-sc2/)
- **sharpy-sc2** — фреймворк быстрого прототипирования ботов (используется Sharpened Edge). [github](https://github.com/DrInfy/sharpy-sc2)
- **pysc2** — интерфейс от DeepMind, ориентирован на ML‑исследования (feature layers, мини‑игры). [aiarena](https://aiarena.net/wiki/bot-development/getting-started/_source/)
- **Дополнения**: SC2MapAnalysis, SC2-Map-Segmentation, queens-sc2, bossman (утилиты для карт и pathfinding).

## ⚙️ C++

- **s2client-api** — официальный C++‑клиент Blizzard. Базовый выбор для низкоуровневого доступа. [blizzard.github](https://blizzard.github.io/s2client-api/md_docs_tutorial1.html)
- **cpp-sc2** — обёртка от сообщества, стандартный C++ API в AI Arena. [aiarena](https://aiarena.net/wiki/bot-development/getting-started/_source/)
- **CommandCenter** — мощный стартовый бот с набором логики (на нем построен MicroMachine). [github](https://github.com/RaphaelRoyerRivard/MicroMachine)

## ☕ Java, .NET, Go, Rust, NodeJS

- **Java: ocraft-s2client** — основной Java‑клиент. [aiarena](https://aiarena.net/wiki/bot-development/getting-started/_source/)
- **.NET: Sharky Framework, Tyr, Schmidt** — набор .NET‑фреймворков и шаблонов.
- **Go: go-sc2ai** — популярная обёртка для Go‑ботов.
- **Rust: rust-sc2** — стандартный инструмент для Rust.
- **NodeJS: node-sc2/core** — основной пакет для JavaScript‑ботов.

---

## 🏛 Обобщение от AI Arena

AI Arena Wiki и список awesome‑sc2‑ai сводят «золотой стандарт» к следующему набору:
- **Python**: python‑sc2 (+ ares/sharpy)
- **C++**: cpp-sc2 / CommandCenter
- **Java**: ocraft
- **Другие**: go-sc2ai, rust-sc2, node-sc2.

---
*Если вы целитесь в Python‑бота, «каноничный» стек сейчас: **python-sc2 + ares-sc2 или sharpy-sc2**.*
