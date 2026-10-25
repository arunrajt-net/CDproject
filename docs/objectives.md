# Project Objectives

## 1. Primary Objectives
The central aim of this project is to implement a robust, educational, and professionally engineered **compiler front-end** for a restricted subset of SQL that demonstrates the classical phases of compiler theory:

1. **Phase 1: Lexical Analysis**
   - Read arbitrary SQL source text and tokenize it into categorical units (Keywords, Identifiers, Numbers, Strings, Operators, Punctuation).
   - Accurately track line and column coordinates for every lexeme.
   - Gracefully handle comments, whitespace, and string escape sequences.

2. **Phase 2: Context-Free Grammar Formalization & Transformation**
   - Formulate a formal Context-Free Grammar (CFG) for the language.
   - Eliminate left recursion to guarantee LL(1) compatibility for top-down parsing.
   - Compute FIRST and FOLLOW sets to mathematically establish grammar determinism.

3. **Phase 3: Syntax Analysis & Recursive Descent Parsing**
   - Implement a hand-written Recursive Descent Parser without relying on external parser generators (such as Lex/Yacc or ANTLR).
   - Enforce clause ordering: `SELECT` $\to$ `FROM` $\to$ `WHERE` $\to$ `ORDER BY`.
   - Support boolean expressions with operator precedence (`NOT` > `AND` > `OR`) and parentheses grouping.

4. **Phase 4: Dynamic Parse Tree & AST Construction**
   - Generate a Concrete Syntax Tree (CST) capturing every grammar derivation step.
   - Construct a simplified Abstract Syntax Tree (AST) capturing semantic intent.
   - Serialize both trees to JSON and render clean ASCII/Unicode text trees.

5. **Phase 5: Semantic Analysis & Symbol Table Management**
   - Maintain an in-memory Symbol Table holding schema definitions (tables, columns, data types).
   - Verify table existence, column resolution, and data-type compatibility.
   - Provide fuzzy typo matching to suggest correct table/column names.

6. **Phase 6: Multi-Tier Diagnostic Error Handling**
   - Provide meaningful, user-friendly error diagnostics with line/column localization and corrective recommendations for Lexical, Syntax, and Semantic failures.

7. **Phase 7: Full-Stack Integration & Developer GUI**
   - Deliver a modern Flask-based web application with dark-mode aesthetic, code editor, live pipeline indicators, and inspection tabs.

8. **Phase 8: Automated Verification & Test Coverage**
   - Validate the compiler across a comprehensive benchmark of valid and invalid queries using Pytest and unittest with 100% pass rate.
