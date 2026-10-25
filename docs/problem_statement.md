# Problem Statement

## 1. Academic Context
Undergraduate courses in Compiler Design frequently focus heavily on abstract formalisms—such as regular expressions, finite automata, pushdown automata, and CFGs—often demonstrated solely through basic arithmetic calculators or rudimentary toy languages.

Students rarely get the opportunity to see how compiler front-end techniques apply to real-world domain-specific languages like SQL. SQL queries are structurally unique:
- They are declarative rather than imperative.
- They enforce strict, non-negotiable clause sequences (`SELECT`, `FROM`, `WHERE`, `ORDER BY`).
- They require compound condition parsing with non-trivial operator precedence.
- They demand semantic validation against an external schema dictionary (symbol table).

---

## 2. The Core Problem
To bridge this gap, the assigned problem requires designing and implementing a **functional compiler front-end** that:

1. Takes raw SQL queries written in various styles (mixed casing, multi-line indentation, inline comments).
2. Scans the stream for valid tokens while identifying illegal characters and malformed literals.
3. Verifies that the query conforms to an unambiguous grammar using predictive top-down parsing.
4. Generates an authentic, dynamically produced Parse Tree (CST) and Abstract Syntax Tree (AST) representing the exact syntactic structure of the query.
5. Performs semantic verification against a mock database schema without executing actual database queries on a storage engine.
6. Clearly flags and localizes errors, distinguishing whether an error is Lexical (malformed token), Syntactic (grammar violation), or Semantic (schema inconsistency).

---

## 3. Boundary & Non-Goals
To maintain strict adherence to the project description:
- **This is a Front-End Compiler:** It converts SQL queries into an internal validated AST representation.
- **Not a DBMS Engine:** It does not implement B-Trees, buffer pools, disk storage, or query execution plans.
- **Not a Code Generator:** It does not emit machine instructions or assembly code; the compilation culminates in validated AST data structures and diagnostics.
