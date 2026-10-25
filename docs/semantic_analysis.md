# Semantic Analysis and Symbol Table

## 1. Principles of Semantic Analysis
A syntactically valid query may still be logically and semantically meaningless. For example:
```sql
SELECT salary FROM students;
```
Syntactically, this query adheres perfectly to the CFG (`SELECT <col> FROM <tbl>;`). However, in our database schema, `students` has no column named `salary` (which belongs to `employees`).

The **Semantic Analyzer** (`compiler/semantic_analyzer.py`) bridges this gap by checking static contextual validity against the **Symbol Table** (`compiler/symbol_table.py`).

---

## 2. In-Memory Database Schema (Symbol Table)
The Symbol Table is initialized from `schema/sample_schema.json`:

### Table: `students`
| Column Name | Data Type | Nullable | Key |
|---|---|---|---|
| `id` | `INT` | No | Primary Key |
| `name` | `VARCHAR` | No | - |
| `age` | `INT` | Yes | - |
| `department` | `VARCHAR` | Yes | - |
| `marks` | `FLOAT` | Yes | - |

### Table: `employees`
| Column Name | Data Type | Nullable | Key |
|---|---|---|---|
| `id` | `INT` | No | Primary Key |
| `name` | `VARCHAR` | No | - |
| `salary` | `FLOAT` | Yes | - |
| `department` | `VARCHAR` | Yes | - |

---

## 3. Semantic Validations Performed

1. **Table Resolution:**
   - Checks if the table in `FROM` exists in the Symbol Table.
   - If invalid: `SemanticError: Table 'unknown' does not exist in database schema.`
2. **Projection Resolution (SELECT):**
   - If wildcard `*` is specified, it validates and expands to all schema columns.
   - For named columns, verifies each column exists in the target table.
   - If missing: `SemanticError: Column 'salary' does not exist in table 'students'.`
3. **Filter Resolution (WHERE):**
   - Recursively traverses condition expressions.
   - Verifies that any column referenced in a comparison exists in the queried table.
4. **Ordering Resolution (ORDER BY):**
   - Verifies each column in the `ORDER BY` list exists in the target table.
5. **Data Type Compatibility Checking:**
   - In comparisons, checks the data types of both operands.
   - Compares numeric types (`INT`, `FLOAT`) safely against numbers.
   - Compares string types (`VARCHAR`) safely against strings.
   - Flags invalid cross-type comparisons (e.g. `age = 'twenty'`):
     `SemanticError: Type mismatch in condition: cannot compare INT ('age') with VARCHAR ('twenty')`
6. **Fuzzy Did-You-Mean Suggestions:**
   - If a typo occurs (e.g. `SELECT deparment FROM students`), the Symbol Table runs difflib pattern matching and suggests: `Did you mean 'department'?`
