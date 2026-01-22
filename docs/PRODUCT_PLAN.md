# Product Plan: StarCraft II AI Agent Evolution

## 1. Vision
To develop a competitive StarCraft II AI agent capable of high-level macro-management and adaptive tactical decision-making. The project will demonstrate the application of complex algorithms in a high-dimensional, real-time environment.

---

## 2. Strategic Pillars

### A. Macro Mastery (Economy)
The foundation of any SC2 win. The agent must:
- Optimize worker production (saturation).
- Manage supply (never get "supply blocked").
- Execute timely expansions (taking new bases).
- Maintain a balanced tech tree.

### B. Micro Management (Tactics)
Winning battles with fewer resources:
- Kiting (hit and run).
- Target firing (focusing high-value units).
- Ability usage (Blinks, Storms, Forcefields).
- Intelligent retreat (preserving units).

### C. Scouting & Adaptation
Reacting to the opponent:
- Detecting enemy tech (e.g., seeing a Spire means building anti-air).
- Monitoring army movements.
- Adaptive build orders based on the opponent's race and strategy.

---

## 3. Technology Stack (2026 Context)
- **Language:** Python 3.11+
- **Core Library:** `python-sc2` (BurnySC2) - High-level wrapper over Blizzard's SC2API.
- **Decision Engine:** Initially State-Machine based, evolving into Utility-AI or Reinforcement Learning.
- **Data Analysis:** Analysis of own replays to find timing gaps.

---

## 4. Development Roadmap

### Phase 1: The "Hello World" Bot (Protoss Rush)
- **Goal:** Build a bot that can successfully produce workers and a Zealot army to attack the enemy.
- **Deliverables:** Basic build order, automated worker production, simple "attack-move" logic.

### Phase 2: Macro & Expansion
- **Goal:** Manage multiple bases.
- **Deliverables:** Logic for taking a "Natural" expansion, Vespene gas management, and Gateway-to-Warp-Gate transition.

### Phase 3: Tactical Intelligence (Micro)
- **Goal:** Effective combat.
- **Deliverables:** Stalker kiting, focus-fire logic, and basic army composition (Stalkers + Immortals).

### Phase 4: Scouting & Response
- **Goal:** Intelligence-driven play.
- **Deliverables:** Scout unit logic (Probe/Observer), enemy building detection, and build-order switching.

### Phase 5: Optimization & Competition
- **Goal:** Competitive play on the SC2AI ladder.
- **Deliverables:** Performance profiling, advanced unit control, and participating in community tournaments.

---
© 2026 NEXTTHINGDONE. Built for the SC2 AI community.
