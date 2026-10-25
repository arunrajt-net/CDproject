# Language Specification: Mini SQL Compiler

## 1. Overview
The **Mini SQL Compiler** defines and recognizes a formal restricted subset of the Structured Query Language (SQL), tailored specifically for academic compiler design demonstrations in B.Tech Computer Science.

The target language models the read-only projection, selection, and sorting capabilities of SQL:
- `SELECT` projection (with optional `DISTINCT` and wildcard `*`)
- `FROM` data source specification (with optional table aliases)
- `WHERE` conditional filtering (with comparison and boolean logical operators)
- `ORDER BY` sorting (with single or multiple columns and ascending/descending directions)

---

## 2. Lexical Specification

### 2.1 Character Set & Case Insensitivity
- The language is case-insensitive with respect to SQL keywords. For example, `SELECT`, `select`, and `SeLeCt` produce the exact same keyword token.
- Table and column identifiers are matched case-insensitively during semantic analysis.

### 2.2 Reserved Keywords
The compiler recognizes 11 reserved keywords:
```
SELECT      DISTINCT    FROM        WHERE       ORDER
BY          ASC         DESC        AND         OR
NOT
```

### 2.3 Identifiers
Identifiers name database tables, columns, and aliases:
- **Pattern:** `[a-zA-Z_][a-zA-Z0-9_]*`
- **Examples:** `students`, `age`, `marks`, `department`, `emp_2026`, `s`
- Identifiers cannot begin with numeric digits (e.g. `123students` is an error).

### 2.4 Literals
1. **Integer Literals:**
   - One or more decimal digits: `[0-9]+`
   - Examples: `18`, `0`, `42`, `100`
2. **Floating-Point Literals:**
   - Digits followed by a decimal point and fractional digits: `[0-9]+\.[0-9]+`
   - Examples: `80.5`, `3.1415`, `50000.0`
3. **String Literals:**
   - Enclosed within single quotes: `'...'`
   - Supported escape sequences:
     - `\'` : Single quote
     - `\"` : Double quote
     - `\\` : Backslash
     - `\n` : Newline
     - `\t` : Tab
     - `\r` : Carriage return
   - Unterminated strings raise a diagnostic `LexicalError`.

### 2.5 Operators & Punctuation
- **Comparison Operators:** `=`, `!=`, `<>`, `<`, `<=`, `>`, `>=`
- **Logical Operators:** `AND`, `OR`, `NOT`
- **Punctuation:**
  - `,` : Comma (column and ordering separator)
  - `;` : Semicolon (optional statement terminator)
  - `*` : Asterisk (all-columns wildcard)
  - `(` : Left Parenthesis (condition grouping)
  - `)` : Right Parenthesis (condition grouping)

### 2.6 Comments & Whitespace
- Single-line comments: `-- Comment text up to newline`
- Multi-line block comments: `/* Block comment */`
- Whitespace characters (spaces, tabs, newlines) separate tokens and are discarded by the lexer.

---

## 3. Syntactic Clause Ordering
The parser strictly enforces the canonical SQL clause sequence:
$$\text{SELECT} \longrightarrow \text{FROM} \longrightarrow [\text{WHERE}] \longrightarrow [\text{ORDER BY}] \longrightarrow [;]$$

Violating this order (such as placing `WHERE` after `ORDER BY` or placing `FROM` before `SELECT`) results in an explicit syntax error.

---

## 4. Unsupported Features (Out of Scope)
The following SQL features are intentionally excluded to keep the language amenable to an LL(1) / Recursive Descent parser:
- Data Modification / DDL (`INSERT`, `UPDATE`, `DELETE`, `CREATE`, `DROP`, `ALTER`)
- Table Joins (`INNER JOIN`, `LEFT JOIN`, `CROSS JOIN`)
- Aggregate Functions & Grouping (`COUNT`, `SUM`, `AVG`, `GROUP BY`, `HAVING`)
- Subqueries / Nested Queries (`SELECT ... WHERE id IN (SELECT ...)`)
- Window Functions & CTEs (`OVER()`, `WITH ... AS`)
