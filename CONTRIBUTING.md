# Contributing to Mini SQL Compiler

Welcome to the **Mini SQL Compiler** group project! This document outlines our team workflow, branch standards, and collaboration procedures to ensure smooth development.

---

## 1. Quick Setup for Teammates

### Step 1: Clone the Repository
Clone the repository to your local machine:
```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd mini-sql-compiler
```

### Step 2: Set Up Virtual Environment & Dependencies
Create and activate an isolated Python virtual environment:

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**On Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 2. Git Feature Branch Workflow

Always work on dedicated feature branches. Never commit directly to the `main` or `master` branch.

### Step 1: Synchronize with Remote
Before creating a new feature branch, ensure your local main branch is up to date:
```bash
git checkout master
git pull origin master
```

### Step 2: Create a Feature Branch
Use descriptive branch naming (e.g. `feature/lexer-comments`, `fix/order-by-syntax`, `docs/viva-answers`):
```bash
git checkout -b feature/your-feature
```

### Step 3: Make Your Changes & Run Tests
Make code edits or additions. Before committing, always verify that all automated unit and integration tests pass:
```bash
python -m pytest -v
```

### Step 4: Stage & Commit Changes
Write clear, imperative commit messages:
```bash
git add .
git commit -m "Add your feature"
```

### Step 5: Push Branch to GitHub
```bash
git push origin feature/your-feature
```

### Step 6: Create a Pull Request (PR)
1. Open the repository on GitHub in your web browser.
2. Click **Compare & pull request**.
3. Add a concise description of your changes and tag your module partner for review.
4. Once reviewed and tests pass, merge into the main branch.

---

## 3. Inviting Team Members on GitHub

To grant write access to teammates:
1. Navigate to your repository on GitHub.
2. Click **Settings** (top navigation bar).
3. In the left sidebar, click **Collaborators** under *Access*.
4. Click the green button: **Add people**.
5. Enter your teammate's GitHub username or email address and send the invitation.
6. Teammates must accept the email invitation or accept via `https://github.com/YOUR_USERNAME/mini-sql-compiler/invitations`.

---

## 4. Coding & Architecture Standards

1. **Modular Design:** Keep lexing in `compiler/lexer.py`, parsing in `compiler/parser.py`, and semantic checks in `compiler/semantic_analyzer.py`.
2. **Error Localization:** When raising errors, always provide `line`, `column`, and a helpful `suggestion`.
3. **No Hardcoding:** Parse trees and token streams must be dynamically generated from input queries.
4. **Testing Obligation:** If you modify grammar rules or add features, write matching unit tests under `tests/`.
