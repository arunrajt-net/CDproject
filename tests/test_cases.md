# Automated Test Cases and Execution Evidence

This document records the official benchmark test suite for the **Mini SQL Compiler**, covering Lexical Analysis, Syntax Analysis, Parse Tree Generation, and Semantic Validation.

## Summary of Test Results

- **Total Test Cases Executed:** 60
- **Total Tests Passed:** 60
- **Total Tests Failed:** 0
- **Test Success Rate:** 100.0%
- **Execution Engine:** Pytest 9.1.1 & Python 3.14 Standard `unittest`
- **Execution Time:** ~0.09s

---

## 1. Valid Query Test Suite

| Test ID | SQL Query Input | Expected Output | Actual Output | Phase Validated | Status |
|---|---|---|---|---|---|
| **TC-VAL-01** | `SELECT * FROM students;` | Success (Wildcard select) | Successfully Compiled, 0 Errors | Lexer, Parser, Semantic | **PASS** |
| **TC-VAL-02** | `SELECT name FROM students;` | Success (Single column) | Successfully Compiled, 0 Errors | Lexer, Parser, Semantic | **PASS** |
| **TC-VAL-03** | `SELECT name, age FROM students WHERE age > 18;` | Success (Simple numeric condition) | Successfully Compiled, 0 Errors | Lexer, Parser, Semantic | **PASS** |
| **TC-VAL-04** | `SELECT name FROM students ORDER BY age DESC;` | Success (Explicit descending order) | Successfully Compiled, 0 Errors | Lexer, Parser, Semantic | **PASS** |
| **TC-VAL-05** | `SELECT name, marks FROM students WHERE marks >= 80 ORDER BY marks ASC;` | Success (WHERE + ORDER BY combined) | Successfully Compiled, 0 Errors | Lexer, Parser, Semantic | **PASS** |
| **TC-VAL-06** | `SELECT name FROM students WHERE age > 18 AND department = 'CSE';` | Success (Compound AND condition) | Successfully Compiled, 0 Errors | Lexer, Parser, Semantic | **PASS** |
| **TC-VAL-07** | `SELECT name FROM employees WHERE salary > 30000;` | Success (Alternate table and float salary) | Successfully Compiled, 0 Errors | Lexer, Parser, Semantic | **PASS** |
| **TC-VAL-08** | `SELECT * FROM students WHERE age >= 18 OR marks > 80 ORDER BY age;` | Success (OR logic + default ASC order) | Successfully Compiled, 0 Errors | Lexer, Parser, Semantic | **PASS** |
| **TC-VAL-09** | `SELECT DISTINCT department FROM employees;` | Success (Optional DISTINCT keyword) | Successfully Compiled, 0 Errors | Lexer, Parser, Semantic | **PASS** |
| **TC-VAL-10** | `SELECT name FROM students s;` | Success (Optional table alias) | Successfully Compiled, 0 Errors | Lexer, Parser, Semantic | **PASS** |
| **TC-VAL-11** | `SELECT * FROM students WHERE NOT age < 18;` | Success (Unary NOT logical operator) | Successfully Compiled, 0 Errors | Lexer, Parser, Semantic | **PASS** |
| **TC-VAL-12** | `select NAME, AGE from STUDENTS where AGE > 18;` | Success (Case-insensitivity verification) | Successfully Compiled, 0 Errors | Lexer, Parser, Semantic | **PASS** |

---

## 2. Invalid Query Diagnostic Test Suite

| Test ID | SQL Query Input | Expected Error Type | Actual Error Message | Line:Col | Status |
|---|---|---|---|---|---|
| **TC-INV-01** | `SELECT FROM students;` | Syntax Error | Missing column list or wildcard '*' in SELECT clause | Line 1:8 | **PASS** |
| **TC-INV-02** | `SELECT name students;` | Syntax Error | Expected 'FROM' keyword following SELECT clause, got 'students' | Line 1:13 | **PASS** |
| **TC-INV-03** | `SELECT name FROM;` | Syntax Error | Missing table name in FROM clause | Line 1:17 | **PASS** |
| **TC-INV-04** | `SELECT name FROM students WHERE;` | Syntax Error | Missing search condition after WHERE keyword | Line 1:33 | **PASS** |
| **TC-INV-05** | `SELECT name FROM students ORDER BY;` | Syntax Error | Missing sorting column after ORDER BY keyword | Line 1:36 | **PASS** |
| **TC-INV-06** | `SELECT unknown_column FROM students;` | Semantic Error | Column 'unknown_column' does not exist in table 'students' | Line 1:8 | **PASS** |
| **TC-INV-07** | `SELECT name FROM unknown_table;` | Semantic Error | Table 'unknown_table' does not exist in database schema | Line 1:18 | **PASS** |
| **TC-INV-08** | `SELECT name FROM students WHERE age >;` | Syntax Error | Missing right-hand operand after comparison operator '>' | Line 1:38 | **PASS** |
| **TC-INV-09** | `SELECT name FROM students @;` | Lexical Error | Unrecognized or invalid character '@' in SQL query | Line 1:27 | **PASS** |
| **TC-INV-10** | `SELECT name, FROM students;` | Syntax Error | Trailing comma in SELECT column list with no following column | Line 1:12 | **PASS** |
| **TC-INV-11** | `SELECT * FROM students WHERE name = 'John` | Lexical Error | Unterminated string literal: missing closing single quote | Line 1:38 | **PASS** |
| **TC-INV-12** | `SELECT name FROM students WHERE age = 'twenty';` | Semantic Error | Type mismatch in condition: cannot compare INT ('age') with VARCHAR ('twenty') | Line 1:38 | **PASS** |
| **TC-INV-13** | `SELECT name FROM students ORDER BY age WHERE age > 18;` | Syntax Error | WHERE clause cannot appear after ORDER BY clause | Line 1:41 | **PASS** |
| **TC-INV-14** | `SELECT 123student FROM students;` | Lexical Error | Invalid numeric literal or identifier '123student': identifiers cannot start with numbers | Line 1:8 | **PASS** |
| **TC-INV-15** | `   ` | Syntax Error | Empty query provided: SQL statement cannot be blank | Line 1:1 | **PASS** |

---

## 3. Component Test Breakdown

1. **`test_lexer.py` (10 tests)**:
   - Case-insensitivity for all 11 keywords
   - Integers, decimals, and alphanumeric identifiers
   - String literals with escape characters (`\'`, `\"`, `\\`, `\n`, `\t`)
   - Comparison operators (`=`, `!=`, `<>`, `<`, `<=`, `>`, `>=`)
   - Delimiters and wildcard (`*`, `,`, `;`, `(`, `)`)
   - Line and column coordinates tracking across multiline statements
   - SQL comments skipping (`--` and `/* ... */`)
   - Detection of illegal symbols, unterminated strings, and invalid number prefixes

2. **`test_parser.py` (18 tests)**:
   - Recursive descent CFG productions
   - Wildcards, multi-column selections, DISTINCT
   - Table aliasing
   - Boolean precedence: NOT > AND > OR, with parentheses grouping
   - Multiple ORDER BY columns with ASC/DESC
   - Accurate syntax error localization and actionable diagnostics

3. **`test_parse_tree.py` (5 tests)**:
   - Concrete Syntax Tree (CST) hierarchy and node tagging
   - Parent-child tree linkage
   - JSON serialization for Web UI
   - ASCII and Unicode tree formatting
   - Abstract Syntax Tree (AST) structure isolation

4. **`test_semantic.py` (7 tests)**:
   - Mock schema loading from JSON
   - Table existence checking
   - Column existence checking (SELECT, WHERE, ORDER BY)
   - Type compatibility validation (e.g., numeric vs VARCHAR)
   - Fuzzy typo matching and column/table suggestions

5. **`test_compiler.py` (20 tests)**:
   - End-to-end integration across all 8 required valid queries
   - End-to-end integration across all 10 required invalid queries
   - Multiline queries with embedded comments
   - Phase status flags (`PASSED`, `FAILED`, `SKIPPED`)
