# Contributing to SIADA+ Evolution 🚀

Thank you for your interest in contributing to **SIADA+ Evolution**, an open-source academic scheduling and combinatorial optimization platform built for public vocational training institutions (SENA).

We welcome contributions from operations research engineers, Python developers, academic coordinators, and AI researchers!

## 🛠️ How Can You Contribute?

### 1. Reporting Bugs & Scheduling Edge Cases
If you encounter an `INFEASIBLE` state with valid datasets or find a bug in the constraint solver:
- Open a **GitHub Issue** describing the dataset dimensions (cohorts, instructors, rooms) and the specific constraint involved.
- **Important:** Never attach Excel files containing real personal data (names, IDs, or phone numbers). Always use anonymized datasets.

### 2. Suggesting New Constraints & Features
We are actively expanding the mathematical model (`CP-SAT`) and the cognitive AI layer (`Claude API`). High-priority areas include:
- Multi-day continuous blocks per learning outcome (*Resultados de Aprendizaje*).
- Classroom capacity and specialized equipment matching (e.g., laboratories vs. standard rooms).
- Natural language prompt templates for dynamic instructor reassignments.

### 3. Submitting Pull Requests (PRs)
1. **Fork** the repository and create a new branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Follow clean code practices:** Keep mathematical constraints modular inside `solver.py` and UI logic inside `app.py`.
3. **Test locally** using the sample datasets in `/ejemplos`:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```
4. Submit a **Pull Request** with a clear description of the mathematical or functional improvement.

## 📜 Code of Conduct
This project fosters an open, collaborative, and respectful environment dedicated to improving public education through open-source technology.
