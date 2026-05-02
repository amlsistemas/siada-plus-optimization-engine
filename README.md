---
title: SIADA+ Evolution v6.1 - AI-Powered Academic Orchestrator
emoji: 📅
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: mit
short_description: Advanced academic scheduling optimization using CP-SAT and Claude 3.5
tags:
  - streamlit
  - optimization
  - cp-sat
  - sena
  - anthropic-claude
---

# SIADA+ Evolution v6.1 🚀
### Intelligent System for Teacher and Environment Assignment

**SIADA+ Evolution** is an advanced open-source optimization engine designed for large-scale vocational training centers (SENA). It transitions from legacy heuristics to **Mathematical Constraint Programming (CP-SAT)** and **Generative AI reasoning**.

## 🧠 Technical Core
- **Optimization Engine:** Powered by Google OR-Tools CP-SAT Solver.
- **Reasoning Layer:** Integration with **Anthropic Claude 3.5 Sonnet** (vía API) to translate natural language constraints into mathematical parameters.
- **Mathematical Model:** Solves an NP-Hard combinatorial problem with $x[i, d, g]$ binary decision variables.

## ✨ Key Features
- **Strict Compliance:** Enforces labor laws (40h/week, max days/week).
- **Dynamic Context:** Handles holiday APIs and specific instructor exclusions.
- **Smart Reassignment:** AI-driven conflict resolution for last-minute changes.
- **Human-Centric:** Designed to reduce 200+ hours of manual coordination per week.

## 🛠 Installation & Usage
1. **Cloud Execution:** Simply upload the 4 required Excel files (Groups, Instructors, Environments, Curriculum).
2. **Local Setup:**
   ```bash
   pip install -r requisitos.txt
   streamlit run aplicación.py
   ```

## 🚀 Roadmap (Vision)
- **v6.2:** Full Natural Language interface via Claude 3.5.
- **v7.0:** Predictive workload analysis and multi-campus orchestration.

---
*Developed by Alejandro Martinez Lopera - ADSO Technologist (SENA Quindío)*
