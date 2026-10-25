# Project Introduction

## 1. Project Background
In the study of Computer Science and Engineering, **Compiler Design** is one of the most foundational subjects, illustrating how high-level, human-readable symbolic languages are validated, translated, and structured into formal representations.

While general-purpose compilers (like GCC, Clang, or Python's bytecode compiler) target complex procedural or object-oriented languages, domain-specific compilers are equally vital in modern software systems. The Structured Query Language (SQL) is the global standard for declarative data querying, and every modern Database Management System (such as PostgreSQL, SQLite, MySQL, and Google BigQuery) incorporates a dedicated **SQL Compiler Front-End** to parse, validate, and optimize incoming query statements before physical execution.

---

## 2. Topic Assignment: Topic 10 – Mini SQL Compiler
The objective assigned for this 5th-semester B.Tech Computer Science group project is:

> *"Develop a compiler front end that recognizes a restricted subset of SQL, including SELECT, FROM, WHERE, and ORDER BY. Validate query syntax and construct a parse tree."*

To satisfy this mandate, our team has built the **Mini SQL Compiler**—a modular, production-ready compiler front end written in **Python 3**, featuring a **Recursive Descent Parser**, an interactive **Flask Web GUI**, and end-to-end automated testing.

---

## 3. Core Highlights of the System
- **Strictly Modular Architecture:** Independent modules for Lexing (`lexer.py`), Grammar definition (`grammar.py`), Parsing (`parser.py`), Parse Tree generation (`parse_tree.py`), Semantic validation (`semantic_analyzer.py`), and Symbol Table management (`symbol_table.py`).
- **Dynamic Concrete & Abstract Trees:** Constructs real Concrete Syntax Trees (CSTs) and Abstract Syntax Trees (ASTs) dynamically from the input query string, rendered both as hierarchical text and structured JSON.
- **Three-Tier Error Diagnosis:** Precision diagnostics categorizing errors into Lexical, Syntax, and Semantic errors with exact 1-based line/column coordinates and actionable suggestions.
- **Professional Web Interface:** A sleek developer UI with an SQL code editor, token inspector, live parse tree viewer, semantic checklist, and preset query loader.
