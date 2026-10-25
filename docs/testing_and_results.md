# Testing and Results Report

## 1. Test Methodology
To ensure high software reliability, test-driven development (TDD) principles were utilized throughout the development of the **Mini SQL Compiler**:
- **Unit Testing:** Individual components (`lexer`, `parser`, `parse_tree`, `semantic_analyzer`, `symbol_table`) are isolated and validated in separate test modules under `tests/`.
- **Integration Testing:** End-to-end compilation runs are validated in `tests/test_compiler.py` covering multi-phase interaction.
- **Benchmark Test Suite:** All 8 mandated valid queries and 10 mandated invalid queries from the specification are verified.

---

## 2. Automated Test Execution Summary

The test suite was executed using Pytest 9.1.1 on Python 3.14.5:

```bash
$ python -m pytest -v
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

- **Total Test Cases:** 60
- **Total Passed:** 60
- **Total Failed:** 0
- **Success Rate:** 100.0%
- **Execution Time:** ~90 milliseconds

---

## 3. Benchmark Verification Matrix

### 3.1 Mandated Valid Queries (All Passed)
1. `SELECT * FROM students;` $\implies$ Success (Wildcard expansion)
2. `SELECT name FROM students;` $\implies$ Success (Single column projection)
3. `SELECT name, age FROM students WHERE age > 18;` $\implies$ Success (Numeric comparison)
4. `SELECT name FROM students ORDER BY age DESC;` $\implies$ Success (Descending sort)
5. `SELECT name, marks FROM students WHERE marks >= 80 ORDER BY marks ASC;` $\implies$ Success (Filter + Sort)
6. `SELECT name FROM students WHERE age > 18 AND department = 'CSE';` $\implies$ Success (Compound AND)
7. `SELECT name FROM employees WHERE salary > 30000;` $\implies$ Success (Float literal comparison)
8. `SELECT * FROM students WHERE age >= 18 OR marks > 80 ORDER BY age;` $\implies$ Success (Compound OR + default ASC)

### 3.2 Mandated Invalid Queries (All Diagnostics Caught)
1. `SELECT FROM students;` $\implies$ Caught `Syntax Error: Missing column list or wildcard`
2. `SELECT name students;` $\implies$ Caught `Syntax Error: Expected 'FROM' keyword`
3. `SELECT name FROM;` $\implies$ Caught `Syntax Error: Missing table name in FROM clause`
4. `SELECT name FROM students WHERE;` $\implies$ Caught `Syntax Error: Missing search condition after WHERE`
5. `SELECT name FROM students ORDER BY;` $\implies$ Caught `Syntax Error: Missing sorting column after ORDER BY`
6. `SELECT unknown_column FROM students;` $\implies$ Caught `Semantic Error: Column 'unknown_column' does not exist`
7. `SELECT name FROM unknown_table;` $\implies$ Caught `Semantic Error: Table 'unknown_table' does not exist`
8. `SELECT name FROM students WHERE age >;` $\implies$ Caught `Syntax Error: Missing right-hand operand`
9. `SELECT name FROM students @;` $\implies$ Caught `Lexical Error: Unrecognized or invalid character '@'`
10. `SELECT name, FROM students;` $\implies$ Caught `Syntax Error: Trailing comma in SELECT column list`
