# StarCraft II AI Agent 🚀

A high-performance AI agent for StarCraft II built with Python. This project aims to bridge the gap between simple scripted behavior and advanced autonomous strategy.

---

## 🛠 Prerequisites & Installation

### 1. Install StarCraft II
You must have the StarCraft II game installed on your system.
- **Mac/Windows:** Install via the [Battle.net Desktop App](https://www.blizzard.com/en-us/download/). It is free to play.
- **macOS Notes:** 
    - The game runs perfectly on **Apple Silicon (M1/M2/M3)** via Rosetta 2.
    - By default, `python-sc2` looks for the game in `/Applications/StarCraft II`.
    - If you installed it elsewhere, set the `SC2PATH` environment variable: `export SC2PATH="/your/custom/path/StarCraft II"`.

### 2. Download Maps
Bots need specific maps to play on. 
1. Download the official Blizzard Map Packs from [SC2 AI Maps](https://github.com/Blizzard/s2client-proto#map-packs).
2. Extract them into your StarCraft II `Maps` folder (e.g., `/Applications/StarCraft II/Maps`).
3. **Password:** Most map packs use the password `iagreetotheeula`.

### 3. Setup Python Environment
We use `python-sc2` (BurnySC2), the most robust library for SC2 bot development.

```bash
# Navigate to the project folder
cd sc2-ai-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install core library
pip install sc2
```

---

## 🚀 Running Your First Bot

We have provided a template bot in `bots/hello_world_bot.py`. This bot plays as **Protoss**, builds Probes, and sends Zealots to attack.

### Run via Terminal
```bash
python3 bots/hello_world_bot.py
```

---

## 🏗 Project Structure

- `bots/`: Contains the source code for various AI agents.
- `docs/`: Technical documentation, product plans, and curated resources.
- `docs/RESOURCES.md`: A collection of StarCraft II AI frameworks, APIs, and tutorials.
- `docs/GETTING_STARTED.md`: Step-by-step onboarding from zero to a working bot.
- `docs/BOT_ARCHITECTURE.md`: Detailed technical breakdown of how our Protoss agent works.
- `docs/STANDARD_TOOLSET.md`: Industry standard libraries and frameworks for all languages.
- `docs/ML_BOTS_OVERVIEW.md`: Analysis of Machine Learning approaches in SC2 (AlphaStar, RL, etc).
- `docs/ML_TRAINING_CASES.md`: Detailed case studies of ML architectures and training pipelines.
- `maps/`: (Optional) Local copies of custom maps.
- `replays/`: Where the game saves its .SC2Replay files for later analysis.

---

## 🧠 Key Concepts

### The "Loop" (`on_step`)
Every bot inherits from `sc2.BotAI`. The `on_step` method is called every game frame. This is where the bot makes decisions:
- "Do I have enough minerals for a Pylon?"
- "Is my army large enough to attack?"
- "Where is the enemy?"

### Unit Selection
Selecting units is done via the `self.units` and `self.structures` filters.
Example: `self.units(UnitTypeId.ZEALOT).idle` (finds all Zealots doing nothing).

---

## 🗺 Roadmap
See the detailed [Product Plan](docs/PRODUCT_PLAN.md) for our 5-phase evolution strategy.

---
© 2026 NEXTTHINGDONE.
