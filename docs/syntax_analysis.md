# Syntax Analysis (Parsing)

## 1. Principles of Syntax Analysis
Syntax Analysis is the second phase of a compiler. It accepts the stream of tokens produced by the lexical analyzer and verifies that the tokens adhere to the structural rules specified by a formal **Context-Free Grammar (CFG)**.

The syntax analyzer produces:
1. **Concrete Syntax Tree (CST):** A full derivation tree recording non-terminals, terminals, and syntactic punctuation.
2. **Abstract Syntax Tree (AST):** A condensed semantic tree omitting syntactic punctuation.

---

## 2. Recursive Descent Parsing Technique

The Mini SQL Compiler implements a **Recursive Descent Parser**, which is a top-down predictive parsing technique:
- Every non-terminal in the transformed CFG corresponds directly to a Python method in `compiler/parser.py`.
- Execution begins at the start symbol method: `parse()`.
- The parser inspects the current token using a single lookahead token ($LL(1)$) to make deterministic branching decisions without backtracking.
- If the current token matches the expectation, it is consumed using `_advance()`.
- If an unexpected token or premature EOF occurs, a diagnostic `SyntaxError` is raised with line and column coordinates.

---

## 3. Parsing Methods Implementation Mapping

| CFG Non-Terminal | Corresponding Method in `compiler/parser.py` | Role & Actions |
|---|---|---|
| `Query` | `parse()` | Entry point: verifies `SELECT`, `FROM`, optional `WHERE`, optional `ORDER BY`, optional `;`, and checks for EOF. |
| `SelectClause` | `_parse_select_clause()` | Consumes `SELECT`, checks for optional `DISTINCT`, verifies non-empty column list or wildcard `*`. |
| `FromClause` | `_parse_from_clause()` | Consumes `FROM`, verifies table identifier, and checks for optional table alias. |
| `WhereClauseOpt` | `_parse_where_clause()` | If `WHERE` token exists, consumes it and initiates boolean condition hierarchy. |
| `OrExpr` | `_parse_or_expr()` | Handles lowest boolean precedence (`OR`) via loop. |
| `AndExpr` | `_parse_and_expr()` | Handles conjunction (`AND`) via loop. |
| `NotExpr` | `_parse_not_expr()` | Handles unary negation (`NOT`). |
| `PrimaryCond` | `_parse_primary_cond()` | Handles grouped sub-expressions `(...)` or relational comparisons. |
| `CompExpr` | `_parse_comp_expr()` | Compares two operands with relational operator (`=`, `>`, etc.). |
| `OrderByClauseOpt`| `_parse_order_by_clause()`| Consumes `ORDER BY`, parses comma-separated sorting columns with `ASC`/`DESC`. |

---

## 4. Clause Order Enforcement Mechanism
SQL mandates a strict linear progression of clauses:
1. When parsing starts, `_check(TokenType.KEYWORD, "SELECT")` is verified. If false, an error like *"Query must begin with 'SELECT'"* is emitted.
2. After `SELECT`, `_check(TokenType.KEYWORD, "FROM")` is verified. If absent (e.g. `SELECT name students;`), an error *"Expected 'FROM' keyword following SELECT clause"* is emitted.
3. If an `ORDER BY` clause is processed and subsequent tokens contain `WHERE`, the parser catches the ordering violation and instructs the user: *"WHERE clause cannot appear after ORDER BY clause"*.
