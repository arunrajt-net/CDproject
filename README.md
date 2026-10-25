# Mini SQL Compiler
### A Compiler Front-End for SQL Query Analysis | B.Tech Computer Science Project

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Flask 3.0+](https://img.shields.io/badge/flask-3.1+-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Tests Passing](https://img.shields.io/badge/tests-60%2F60%20passed-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An educational, fully functional, and modular **Compiler Front-End** for a restricted dialect of the **Structured Query Language (SQL)**. Designed and built from scratch for **Compiler Design (CS501 / CS502) - Topic 10**, this project demonstrates the classical phases of compiler theory:
- **Lexical Analysis (Scanner)** with line/col tracking and string escape processing.
- **Context-Free Grammar Formalization & Left-Recursion Elimination** with mathematical FIRST/FOLLOW verification.
- **Top-Down Recursive Descent Parser** enforcing canonical SQL clause ordering.
- **Dynamic Concrete Syntax Tree (Parse Tree)** and **Abstract Syntax Tree (AST)** generators.
- **Semantic Analyzer & In-Memory Symbol Table** validating table existence, column references, and data-type compatibility.
- **Three-Tier Diagnostic Error Engine** reporting Lexical, Syntax, and Semantic errors with 1-based coordinates and corrective suggestions.
- **Modern Developer Web GUI** built with Flask, responsive dark theme, live pipeline ribbons, and tabbed inspectors.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Supported SQL Dialect](#supported-sql-dialect)
3. [Compiler Architecture & Phases](#compiler-architecture--phases)
4. [Technology Stack](#technology-stack)
5. [Directory Structure](#directory-structure)
6. [Installation & Setup](#installation--setup)
7. [Running the Application](#running-the-application)
8. [Automated Testing](#automated-testing)
9. [Example Queries Demonstration](#example-queries-demonstration)
10. [Parse Tree & AST Visualization](#parse-tree--ast-visualization)
11. [Diagnostic Error Reporting](#diagnostic-error-reporting)
12. [Team Collaboration Guide](#team-collaboration-guide)
13. [License](#license)

---

## 1. Project Overview

The objective of this project is to model how modern database systems (e.g., PostgreSQL, SQLite, MySQL) process incoming declarative SQL queries before physical execution:

$$\text{SQL Source Text} \longrightarrow \text{Lexer} \longrightarrow \text{Token Stream} \longrightarrow \text{Parser} \longrightarrow \text{Parse Tree / AST} \longrightarrow \text{Semantic Analyzer} \longrightarrow \text{Symbol Table} \longrightarrow \text{Result}$$

Unlike toy calculators, the Mini SQL Compiler implements a hand-written **LL(1) Recursive Descent Parser** without relying on external parser generators (Lex/Yacc/Bison/ANTLR), giving students complete transparency into the parsing process.

---

## 2. Supported SQL Dialect

The compiler recognizes the following canonical clauses:

```sql
SELECT [DISTINCT] (* | col1, col2, ...)
FROM table_name [alias]
[WHERE condition]
[ORDER BY col1 [ASC | DESC], col2 [ASC | DESC], ...];
```

### Key Language Features:
- **Case Insensitivity:** SQL keywords can be typed in any case (`SELECT`, `select`, `SeLeCt`).
- **Projections:** Wildcard `*` or comma-separated column identifiers. Optional `DISTINCT`.
- **Data Source:** Table identifiers with optional table alias (e.g. `FROM students s`).
- **Filter Conditions:** Relational operators (`=`, `!=`, `<>`, `>`, `<`, `>=`, `<=`), boolean operators (`AND`, `OR`, `NOT`), parentheses grouping `(...)`, integer/float numbers, and escaped string literals (`'CSE'`, `'It\'s ok'`).
- **Sorting:** `ORDER BY` with multiple comma-separated columns and `ASC` / `DESC` directions (defaults to `ASC` if omitted).
- **Comments:** Single-line (`-- ...`) and multi-line (`/* ... */`) comment stripping.

---

## 3. Compiler Architecture & Phases

```
┌────────────────────────────────────────────────────────┐
│                   Raw SQL Query                        │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│   Phase 1: Lexical Analyzer (compiler/lexer.py)        │
│   • DFA token scanner                                  │
│   • Tracks 1-based line & column numbers               │
│   • Strips comments & handles escape characters        │
└───────────────────────────┬────────────────────────────┘
                            │ List[Token]
                            ▼
┌────────────────────────────────────────────────────────┐
│   Phase 2: Syntax Analyzer (compiler/parser.py)        │
│   • Hand-crafted Recursive Descent Parser              │
│   • Based on transformed, non-left-recursive CFG       │
│   • Enforces: SELECT -> FROM -> [WHERE] -> [ORDER BY]  │
└─────────────────────┬───────────────────┬──────────────┘
                      │                   │
                      ▼                   ▼
┌───────────────────────────┐   ┌────────────────────────┐
│ Parse Tree / CST          │   │ Abstract Syntax Tree   │
│ (compiler/parse_tree.py)  │   │ (compiler/ast_nodes.py)│
└───────────────────────────┘   └────────────┬───────────┘
                                             │
                                             ▼
┌───────────────────────────┐   ┌────────────────────────┐
│ Symbol Table (JSON Schema)│──►│ Semantic Analyzer      │
│ (compiler/symbol_table.py)│   │ (semantic_analyzer.py) │
└───────────────────────────┘   └────────────┬───────────┘
                                             │
                                             ▼
                                ┌────────────────────────┐
                                │ CompilationResult      │
                                └────────────────────────┘
```

---

## 4. Technology Stack

| Layer | Technology | Rationale |
|---|---|---|
| **Programming Language** | Python 3.10+ | Clean object-oriented design, rich standard library, expressive data structures. |
| **Backend Framework** | Flask 3.1+ | Lightweight RESTful backend without heavy dependencies. |
| **Parsing Technique** | Recursive Descent ($LL(1)$) | Hand-crafted deterministic parsing with zero external tool dependencies. |
| **Frontend UI** | HTML5, CSS3, Vanilla JS | Sleek, dark-mode developer interface with line numbers and responsive tabs. |
| **Automated Testing** | Pytest & Python `unittest` | Comprehensive unit and integration test coverage across all 60 test cases. |
| **Version Control** | Git & GitHub | Distributed version control and team branch workflows. |

---

## 5. Directory Structure

```
mini-sql-compiler/
├── app.py                      # Flask Application Controller & REST API
├── requirements.txt            # Python Dependencies
├── README.md                   # Project Documentation & Guide
├── CONTRIBUTING.md             # Git Workflow & Collaboration Guide
├── LICENSE                     # MIT License
├── .gitignore                  # Git Exclusion Configuration
│
├── compiler/                   # Core Compiler Package
│   ├── __init__.py             # Module Exports
│   ├── tokens.py               # Token Types & Token Dataclass
│   ├── errors.py               # Error Hierarchy (Lexical/Syntax/Semantic)
│   ├── lexer.py                # Finite-State Lexical Scanner
│   ├── grammar.py              # CFG Definitions, FIRST & FOLLOW Sets
│   ├── parser.py               # LL(1) Recursive Descent Parser
│   ├── parse_tree.py           # Concrete Syntax Tree Node & Visualizer
│   ├── ast_nodes.py            # Abstract Syntax Tree Data Structures
│   ├── symbol_table.py         # Schema Catalog & Fuzzy Typo Matcher
│   ├── semantic_analyzer.py    # Type Compatibility & Scope Checker
│   └── compiler.py             # Master Compiler Coordinator
│
├── frontend/                   # Web User Interface
│   ├── templates/
│   │   └── index.html          # Semantic HTML5 Layout
│   └── static/
│       ├── css/
│       │   └── style.css       # Dark-Mode Styling & Responsive Layout
│       ├── js/
│       │   └── script.js       # Client Controller & Dynamic Tab Handlers
│       └── images/             # Static Assets
│
├── grammar/                    # Formal Grammar Documentation
│   ├── language_specification.md
│   ├── original_grammar.md
│   ├── transformed_grammar.md
│   ├── first_follow_sets.md
│   └── grammar_explanation.md
│
├── schema/
│   └── sample_schema.json      # Mock In-Memory Database Schema
│
├── tests/                      # Automated Test Suite (60 Test Cases)
│   ├── __init__.py
│   ├── test_lexer.py           # Scanner Unit Tests
│   ├── test_parser.py          # Syntax Analysis Unit Tests
│   ├── test_parse_tree.py      # Tree Serialization Unit Tests
│   ├── test_semantic.py        # Schema & Type Verification Unit Tests
│   ├── test_compiler.py        # End-to-End Pipeline Integration Tests
│   └── test_cases.md           # Test Cases Execution Matrix
│
├── docs/                       # Academic Documentation & Reports
│   ├── project_introduction.md
│   ├── objectives.md
│   ├── problem_statement.md
│   ├── system_architecture.md
│   ├── compiler_phases.md
│   ├── lexical_analysis.md
│   ├── syntax_analysis.md
│   ├── parse_tree_explanation.md
│   ├── semantic_analysis.md
│   ├── error_handling.md
│   ├── testing_and_results.md
│   ├── limitations_and_future_scope.md
│   ├── project_report.md
│   ├── viva_questions.md       # 45 Viva Questions & Simple Answers
│   └── individual_contributions.md
│
└── screenshots/
    └── README.md               # Visual UI Layouts & Demonstration Mockups
```

---

## 6. Installation & Setup

### Prerequisites
- Python 3.10 or higher installed on your machine (`python --version`)
- Git installed (`git --version`)

### Step 1: Clone the Repository
```bash
git clone https://github.com/arunrajt-net/CDproject.git
cd CDproject
```

### Step 2: Create a Virtual Environment
**On Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 7. Running the Application

Start the Flask web development server:
```bash
python app.py
```

Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

The web interface will launch, allowing you to enter queries, select pre-configured presets, and inspect generated parse trees, tokens, and diagnostics in real time.

---

## 8. Automated Testing

The project includes 60 automated unit and integration tests covering every compiler phase:

To run the complete test suite:
```bash
python -m pytest -v
```

Or using Python's standard `unittest` test runner:
```bash
python -m unittest discover tests -v
```

### Test Suite Execution Output:
```
============================= test session starts =============================
platform win32 -- Python 3.14.5, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\arunr\Documents\antigravity\sharp-hawking
collected 60 items

tests/test_compiler.py ....................                              [ 33%]
tests/test_lexer.py ..........                                           [ 50%]
tests/test_parse_tree.py .....                                           [ 58%]
tests/test_parser.py ..................                                  [ 88%]
tests/test_semantic.py .......                                           [100%]

============================= 60 passed in 0.09s ==============================
```

---

## 9. Example Queries Demonstration

### Valid Queries (Successfully Compiled)
1. **Wildcard Projection:**
   ```sql
   SELECT * FROM students;
   ```
2. **Numeric Filter & Projections:**
   ```sql
   SELECT name, age FROM students WHERE age > 18;
   ```
3. **Compound Condition & Sorting:**
   ```sql
   SELECT name, marks FROM students WHERE marks >= 80 AND department = 'CSE' ORDER BY marks DESC;
   ```
4. **DISTINCT Selection & Alternate Table:**
   ```sql
   SELECT DISTINCT department FROM employees WHERE salary > 40000.0;
   ```

### Invalid Queries (Caught with Actionable Diagnostics)
1. **Missing Column List (`Syntax Error`):**
   ```sql
   SELECT FROM students;
   -- Diagnostics: Missing column list or wildcard '*' in SELECT clause (Line 1:8)
   ```
2. **Missing FROM Keyword (`Syntax Error`):**
   ```sql
   SELECT name students;
   -- Diagnostics: Expected 'FROM' keyword following SELECT clause (Line 1:13)
   ```
3. **Unknown Column (`Semantic Error`):**
   ```sql
   SELECT salary FROM students;
   -- Diagnostics: Column 'salary' does not exist in table 'students' (Line 1:8)
   ```
4. **Type Mismatch (`Semantic Error`):**
   ```sql
   SELECT name FROM students WHERE age = 'twenty';
   -- Diagnostics: Type mismatch in condition: cannot compare INT ('age') with VARCHAR ('twenty') (Line 1:38)
   ```
5. **Illegal Character (`Lexical Error`):**
   ```sql
   SELECT name FROM students @;
   -- Diagnostics: Unrecognized or invalid character '@' in SQL query (Line 1:27)
   ```

---

## 10. Parse Tree & AST Visualization

For the query:
```sql
SELECT name, age FROM students WHERE age > 18 ORDER BY age DESC;
```

### Generated Concrete Parse Tree (CST):
```
Query
├── SELECT ('SELECT')
│   └── SelectList
│       ├── Identifier ('name')
│       └── Identifier ('age')
├── FROM ('FROM')
│   └── Table ('students')
├── WHERE ('WHERE')
│   └── Condition ('>')
│       ├── Identifier ('age')
│       └── Number ('18')
├── ORDER BY ('ORDER BY')
│   └── OrderItem ('age DESC')
│       ├── Column ('age')
│       └── Direction ('DESC')
└── Semicolon (';')
```

---

## 11. Diagnostic Error Reporting
Every error raised by the compiler inherits from `CompilerError` and outputs:
- **Error Type:** `Lexical Error`, `Syntax Error`, or `Semantic Error`
- **Location:** Exact 1-based `Line` and `Column` coordinates
- **Message:** Clear description of the violation
- **Suggestion:** Actionable fix recommendation (e.g. *"Did you mean 'department'?"*)

---

## 12. Team Collaboration Guide

Refer to [CONTRIBUTING.md](CONTRIBUTING.md) for branch guidelines, pull request procedures, and collaborator permissions.
Refer to [docs/viva_questions.md](docs/viva_questions.md) for 45 comprehensive project viva questions and answers.

---

## 13. License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
