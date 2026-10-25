# Error Detection and Diagnostic Handling

## 1. Diagnostic Architecture
A great compiler does not merely reject invalid input; it acts as a helpful diagnostic tool for the software developer. The **Mini SQL Compiler** features a rigorous three-tiered error diagnosis subsystem (`compiler/errors.py`).

Every diagnostic error provides:
- **`error_type`**: Distinct category (`Lexical Error`, `Syntax Error`, or `Semantic Error`).
- **`message`**: Clear explanation of what went wrong.
- **`line`**: 1-based source line number.
- **`column`**: 1-based source column coordinate.
- **`suggestion`**: Concrete recommendation on how to correct the query.

---

## 2. Error Categorization & Examples

### Tier 1: Lexical Errors (`LexicalError`)
Occur when characters in the query cannot be assembled into valid tokens.

| Sample Query | Diagnostic Message | Suggestion |
|---|---|---|
| `SELECT name FROM students @;` | `Unrecognized or invalid character '@' in SQL query` | `Remove character '@' or replace with valid SQL syntax` |
| `SELECT * FROM students WHERE name = 'John` | `Unterminated string literal: missing closing single quote (')` | `Add a closing single quote (') to terminate the string` |
| `SELECT 123student FROM students;` | `Invalid numeric literal or identifier '123student': identifiers cannot start with numbers` | `Separate number and identifier with whitespace` |

### Tier 2: Syntax Errors (`SyntaxError`)
Occur when tokens violate the Context-Free Grammar.

| Sample Query | Diagnostic Message | Suggestion |
|---|---|---|
| `SELECT FROM students;` | `Missing column list or wildcard '*' in SELECT clause` | `Specify columns (e.g., 'SELECT name, age' or 'SELECT *')` |
| `SELECT name students;` | `Expected 'FROM' keyword following SELECT clause, got 'students'` | `Add 'FROM <table_name>' after the column list` |
| `SELECT name FROM;` | `Missing table name in FROM clause` | `Specify a table name, e.g. 'FROM students'` |
| `SELECT name FROM students WHERE;` | `Missing search condition after WHERE keyword` | `Provide a filtering condition, e.g. 'WHERE age > 18'` |
| `SELECT name FROM students ORDER BY;` | `Missing sorting column after ORDER BY keyword` | `Specify at least one column to sort by` |
| `SELECT name, FROM students;` | `Trailing comma in SELECT column list with no following column` | `Remove the trailing comma or add the next column name` |
| `SELECT name FROM students ORDER BY age WHERE age > 18;` | `WHERE clause cannot appear after ORDER BY clause` | `Move the WHERE clause before the ORDER BY clause` |

### Tier 3: Semantic Errors (`SemanticError`)
Occur when syntactically legal queries conflict with the schema or type rules.

| Sample Query | Diagnostic Message | Suggestion |
|---|---|---|
| `SELECT salary FROM students;` | `Column 'salary' does not exist in table 'students'` | `Available columns in 'students': id, name, age, department, marks` |
| `SELECT name FROM unknown_table;` | `Table 'unknown_table' does not exist in database schema` | `Available tables: students, employees` |
| `SELECT name FROM students WHERE age = 'twenty';` | `Type mismatch in condition: cannot compare INT ('age') with VARCHAR ('twenty')` | `Convert the operand to match compatible data type (INT)` |

---

## 3. Strict Safety Invariant
The compiler guarantees that **a failed query is never marked as successful**. Whenever an error is raised:
1. `res.is_success` is set to `False`.
2. The failing phase is marked as `FAILED`.
3. Subsequent compilation phases are cleanly marked as `SKIPPED`.
4. The error is returned to the user interface and highlighted in the Diagnostics tab.
