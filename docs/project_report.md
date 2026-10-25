# Academic Project Report

# MINI SQL COMPILER
### A Compiler Front-End for SQL Query Analysis

---

**Course:** Compiler Design (CS501 / CS502)  
**Degree:** Bachelor of Technology in Computer Science & Engineering (B.Tech CSE)  
**Semester:** 5th Semester  
**Assigned Topic:** Topic 10 – Mini SQL Compiler  
**Academic Year:** 2026  

---

## 2. Abstract
This project presents the design, formalization, and implementation of **Mini SQL Compiler**, a fully featured compiler front-end developed for a restricted dialect of Structured Query Language (SQL). The compiler processes SQL queries containing `SELECT`, `FROM`, `WHERE`, and `ORDER BY` clauses. The implementation follows standard compiler architecture, featuring a deterministic finite automaton (DFA) based lexical analyzer, an LL(1) non-left-recursive Context-Free Grammar, a top-down Recursive Descent Parser, dynamic Concrete Syntax Tree (CST) and Abstract Syntax Tree (AST) generators, and a static semantic analyzer operating over an in-memory database schema symbol table. The system provides a multi-tiered error diagnostic engine reporting lexical, syntax, and semantic errors with 1-based line/column precision and actionable suggestions. An interactive, dark-themed Flask web interface and an automated 60-test test suite validate the system with a 100% pass rate.

---

## 3. Introduction
SQL is the standard language for querying relational databases worldwide. Behind every enterprise database engine lies a sophisticated compiler front-end that accepts unstructured query strings, verifies their lexical and grammatical legality, validates their references against schema metadata, and produces an internal parse tree for subsequent query optimization. This project demystifies the SQL front-end by implementing each stage from scratch in Python 3 without black-box parser generation libraries.

---

## 4. Problem Statement
Traditional compiler design laboratory projects often focus on toy arithmetic expression evaluators. While instructive, they fail to demonstrate how compilers handle declarative domain-specific languages with rigid clause sequence requirements (`SELECT` $\to$ `FROM` $\to$ `WHERE` $\to$ `ORDER BY`), compound boolean expressions with logical precedence (`NOT` > `AND` > `OR`), and static semantic verification against an external catalog. The objective is to construct an end-to-end compiler front-end that recognizes and validates this SQL subset and outputs a dynamic parse tree.

---

## 5. Objectives
1. Tokenize SQL queries into recognized token categories while tracking exact line/col coordinates.
2. Formalize a Context-Free Grammar (CFG) and eliminate left recursion to allow deterministic LL(1) top-down parsing.
3. Construct a hand-crafted Recursive Descent Parser that strictly enforces clause order.
4. Dynamically build both Concrete Syntax Trees (CST) and Abstract Syntax Trees (AST).
5. Perform semantic analysis (table/column existence, type compatibility) using an in-memory symbol table.
6. Provide clear diagnostic error reporting with line/column localization and fix recommendations.
7. Build a modern web-based developer interface using Flask, HTML5, CSS3, and JavaScript.
8. Achieve 100% test pass rate across benchmark test queries.

---

## 6. Scope
- **In Scope:** `SELECT`, `DISTINCT`, column projections, wildcard `*`, `FROM` with table identifiers and aliases, `WHERE` with comparison operators (`=`, `!=`, `<>`, `<`, `<=`, `>`, `>=`) and logical operators (`AND`, `OR`, `NOT`) with parentheses, `ORDER BY` with `ASC`/`DESC`, comments, and schema validation against mock tables (`students`, `employees`).
- **Out of Scope:** DDL/DML statements (`INSERT`, `CREATE`), multi-table joins (`JOIN`), aggregations (`COUNT`, `SUM`), `GROUP BY`, and physical disk execution.

---

## 7. Language Specification
- **Keywords:** `SELECT`, `DISTINCT`, `FROM`, `WHERE`, `ORDER`, `BY`, `ASC`, `DESC`, `AND`, `OR`, `NOT` (case-insensitive).
- **Identifiers:** `[a-zA-Z_][a-zA-Z0-9_]*`.
- **Literals:** Integers (`[0-9]+`), Floats (`[0-9]+\.[0-9]+`), Strings (`'...'` with escape sequences).
- **Operators & Punctuation:** Comparison operators, logical operators, `,`, `;`, `(`, `)`, `*`.
- **Clause Sequence:** `SELECT` $\to$ `FROM` $\to$ `WHERE` (optional) $\to$ `ORDER BY` (optional) $\to$ `;` (optional).

---

## 8. System Architecture
```
SQL Source Text ──► Lexer ──► Token Stream ──► Parser ──┬──► Concrete Parse Tree (CST)
                                                        └──► Abstract Syntax Tree (AST)
                                                                     │
Schema Catalog (JSON) ──► Symbol Table ──────────────────────────────┴──► Semantic Analyzer
                                                                                │
                                                                                ▼
                                                                       CompilationResult
```

---

## 9. Lexical Analysis
Implemented in `compiler/lexer.py`. It operates as a deterministic scanner maintaining `line` and `column` counters:
- Strips single-line (`--`) and multi-line (`/* ... */`) comments.
- Normalizes keywords to uppercase for case-insensitive matching.
- Validates escape characters in string literals (`\'`, `\"`, `\\`, `\n`, `\t`).
- Detects lexical violations (illegal characters, unterminated strings) and raises `LexicalError`.

---

## 10. Token Generation
Tokens are encapsulated in the `Token` dataclass (`compiler/tokens.py`) with fields `type`, `value`, `line`, `column`, and `literal_value`. Eleven token types are maintained: `KEYWORD`, `IDENTIFIER`, `NUMBER`, `STRING`, `OPERATOR`, `COMMA`, `SEMICOLON`, `LPAREN`, `RPAREN`, `ASTERISK`, `EOF`.

---

## 11. Context-Free Grammar
The original grammar contained left-recursive productions for list structures:
- $\text{ColumnList} \longrightarrow \text{ColumnList} , \text{IDENTIFIER} \mid \text{IDENTIFIER}$
- $\text{OrExpr} \longrightarrow \text{OrExpr} \text{ OR } \text{AndExpr} \mid \text{AndExpr}$
- $\text{AndExpr} \longrightarrow \text{AndExpr} \text{ AND } \text{NotExpr} \mid \text{NotExpr}$
- $\text{OrderList} \longrightarrow \text{OrderList} , \text{OrderItem} \mid \text{OrderItem}$

---

## 12. Grammar Transformation
Using the formal rule $A \to A\alpha \mid \beta \implies A \to \beta A', A' \to \alpha A' \mid \varepsilon$, left recursion was eliminated:
- $\text{ColumnList} \longrightarrow \text{IDENTIFIER } \text{ColumnListTail}$
- $\text{ColumnListTail} \longrightarrow , \text{ IDENTIFIER } \text{ColumnListTail} \mid \varepsilon$
- $\text{OrExpr} \longrightarrow \text{AndExpr } \text{OrExprTail}$
- $\text{OrExprTail} \longrightarrow \text{OR } \text{AndExpr } \text{OrExprTail} \mid \varepsilon$
- $\text{AndExpr} \longrightarrow \text{NotExpr } \text{AndExprTail}$
- $\text{AndExprTail} \longrightarrow \text{AND } \text{NotExpr } \text{AndExprTail} \mid \varepsilon$
- $\text{OrderList} \longrightarrow \text{OrderItem } \text{OrderListTail}$
- $\text{OrderListTail} \longrightarrow , \text{ OrderItem } \text{OrderListTail} \mid \varepsilon$

This rendered the grammar $LL(1)$ compatible with pairwise disjoint FIRST and FOLLOW sets.

---

## 13. Parsing Technique
Implemented in `compiler/parser.py`. The parser uses Recursive Descent with 1-token lookahead. Tail recursive rules are mapped to linear while-loops for maximum efficiency and clean CST node creation.

---

## 14. Parse Tree Construction
- **CST (`compiler/parse_tree.py`):** Captures complete hierarchical derivations, formatted as box-drawing Unicode (`├──`, `└──`) or ASCII trees.
- **AST (`compiler/ast_nodes.py`):** Strips punctuation and builds typed Python AST nodes (`QueryNode`, `SelectClauseNode`, `BinaryOpNode`, etc.) serialized cleanly to JSON.

---

## 15. Semantic Analysis
Implemented in `compiler/semantic_analyzer.py`. Validates:
1. Target table exists in schema.
2. Selected columns exist in table.
3. WHERE condition columns exist in table.
4. ORDER BY columns exist in table.
5. Type compatibility: flags numeric vs. VARCHAR comparisons.

---

## 16. Symbol Table
Implemented in `compiler/symbol_table.py`. Reads schema from `schema/sample_schema.json`. Contains tables `students` and `employees` with metadata for column types (`INT`, `FLOAT`, `VARCHAR`), nullability, and primary keys. Incorporates fuzzy matching to suggest corrections on typos.

---

## 17. Error Detection and Handling
Structured in `compiler/errors.py`:
- `LexicalError`: Invalid characters, unterminated strings.
- `SyntaxError`: Clause order violations, missing keywords/operands.
- `SemanticError`: Missing table/column, cross-type comparisons.
All errors include exact line, column, and actionable suggestions.

---

## 18. Implementation Details
The backend is powered by Flask (`app.py`), exposing `/api/compile`, `/api/schema`, and `/api/examples`. The frontend (`frontend/`) features an IDE-style dark interface with synchronized line numbers, interactive tabbed outputs, and pipeline status ribbons.

---

## 19. Test Cases
The test harness in `tests/` contains 60 automated unit and integration tests across 5 test suites:
- `test_lexer.py` (10 tests)
- `test_parser.py` (18 tests)
- `test_parse_tree.py` (5 tests)
- `test_semantic.py` (7 tests)
- `test_compiler.py` (20 tests)

---

## 20. Test Results
- **All 60 tests passed (100% pass rate).**
- Execution time: 0.09s on Python 3.14.5.
- Verified all 8 required valid queries and 10 required invalid queries.

---

## 21. Screenshots
Screenshots demonstrating the web interface, parse tree generation, token stream inspector, and diagnostic error reports are documented in `screenshots/README.md`.

---

## 22. Limitations
Single-table queries only; no relational joins; read-only querying without DDL/DML; no physical database query execution engine.

---

## 23. Future Enhancements
Support for multi-table `JOIN` operations, aggregate functions (`COUNT`, `SUM`, `AVG`), `GROUP BY`/`HAVING`, and relational algebra intermediate code generation with optimization.

---

## 24. Conclusion
The **Mini SQL Compiler** fulfills all academic objectives set forth for Topic 10. It establishes a complete, working, rigorously tested, and professionally documented compiler front-end for SQL.

---

## 25. References
1. Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Addison-Wesley.
2. Grune, D., & Jacobs, C. J. (2007). *Parsing Techniques: A Practical Guide* (2nd ed.). Springer.
3. Date, C. J. (2003). *An Introduction to Database Systems* (8th ed.). Addison-Wesley.
4. Python Software Foundation. (2026). *Python 3.14 Documentation*.
5. Pallets Projects. (2026). *Flask Documentation (3.1.x)*.
