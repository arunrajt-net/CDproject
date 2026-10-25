# Demonstration Evidence & Interface Visualizations

This directory documents the user interface and visual demonstration artifacts for the **Mini SQL Compiler**.

---

## 1. Web Application Visual Interface

```
+---------------------------------------------------------------------------------------------------------+
| [</>] Mini SQL Compiler v1.0   Compiler Front-End for SQL Query Analysis      (●) Engine Ready   [Schema] |
+---------------------------------------------------------------------------------------------------------+
|                                                   |                                                     |
| [SQL Query Input]            Presets: [Select...] | [1] Lexical: PASSED  ──► [2] Syntax: PASSED ──► [3] |
| +-----------------------------------------------+ | Tokens: 16       Time: 2.3 ms      Result: SUCCESS  |
| | 1 | SELECT name, age                          | +---------------------------------------------------+ |
| | 2 | FROM students                             | | [Parse Tree] [Tokens] [AST/JSON] [Semantic] [Err] | |
| | 3 | WHERE age > 18                            | +---------------------------------------------------+ |
| | 4 | ORDER BY age DESC;                        | | Query                                             | |
| |   |                                           | | ├── SELECT ('SELECT')                             | |
| +-----------------------------------------------+ | | │   └── SelectList                                | |
| [Ctrl + Enter to compile]  [Clear] [Reset] [⚡COMPILE| | │       ├── Identifier ('name')               | |
|                                                   | | │       └── Identifier ('age')                | |
| [Configured Mock Database Schema]                 | | ├── FROM ('FROM')                                 | |
|  [students: id(PK), name, age, dept, marks]       | | │   └── Table ('students')                        | |
|  [employees: id(PK), name, salary, dept]          | | ├── WHERE ('WHERE')                               | |
|                                                   | | │   └── Condition ('>')                           | |
|                                                   | | │       ├── Identifier ('age')                    | |
|                                                   | | │       └── Number ('18')                         | |
|                                                   | | └── ORDER BY ('ORDER BY')                         | |
|                                                   | |     └── OrderItem ('age DESC')                    | |
+---------------------------------------------------+-----------------------------------------------------+
```

---

## 2. Demonstrated Execution Views

### View 1: Parse Tree (CST) View
Displays the full derivation tree produced dynamically by the recursive descent parser with clean branch connectors (`├──`, `└──`).

### View 2: Lexical Token Stream View
Renders an interactive, responsive table with colored badges representing every token extracted:
- `KEYWORD` (Blue badge)
- `IDENTIFIER` (Emerald badge)
- `NUMBER` (Amber badge)
- `STRING` (Pink badge)
- `OPERATOR` (Purple badge)
- `COMMA`, `SEMICOLON` (Gray badge)

### View 3: Abstract Syntax Tree (AST JSON) View
Provides a clean, syntax-colored JSON dump of the underlying semantic `QueryNode` tree structure, complete with line and column coordinates for every AST leaf.

### View 4: Semantic Validation Checklist
Displays an automated audit log verifying:
- Table existence in schema catalog
- Column resolution in `SELECT`
- Column resolution and type compatibility in `WHERE`
- Column resolution in `ORDER BY`

### View 5: Diagnostic Error Reporting
When an invalid query is submitted (e.g. `SELECT salary FROM students;`), the Diagnostics tab automatically activates, displaying:
- Error Category Badge (`Semantic Error`)
- Position Marker (`Line 1, Column 8`)
- Specific Error Message: `Column 'salary' does not exist in table 'students'`
- Actionable Suggestion: `Available columns in 'students': id, name, age, department, marks`
