# Grammar Explanation and Engineering Rationale

## 1. Overview
The grammar of the **Mini SQL Compiler** is designed around classic compiler engineering principles from Aho, Lam, Sethi, and Ullman (the Dragon Book). It structures SQL query syntax into a deterministic, unambiguous LL(1) grammar suitable for hand-written Recursive Descent Parsing.

---

## 2. Operator Precedence Hierarchy in the CFG

In programming language and query compilers, operator precedence is encoded structurally into the grammar hierarchy. Deeper production rules have higher binding power.

Our grammar establishes the following precedence hierarchy:

| Level | Operator Type | Grammar Non-Terminal | Associativity |
|---|---|---|---|
| **1 (Highest)** | Primary / Grouped Expressions | `PrimaryCond` (`(...)`, Operands) | N/A |
| **2** | Relational Comparisons | `CompExpr` (`=`, `!=`, `<>`, `<`, `<=`, `>`, `>=`) | Non-associative |
| **3** | Unary Logical Negation | `NotExpr` (`NOT`) | Right-associative |
| **4** | Conjunction (AND) | `AndExpr` (`AND`) | Left-associative |
| **5 (Lowest)** | Disjunction (OR) | `OrExpr` (`OR`) | Left-associative |

### Why This Matters:
Given the query:
```sql
WHERE age > 18 OR marks > 80 AND department = 'CSE'
```
The parser builds the parse tree such that `marks > 80 AND department = 'CSE'` is grouped first before being evaluated in the `OR` expression, respecting standard boolean operator precedence without requiring artificial disambiguation rules.

---

## 3. Simulating Tail Recursion with Iterative While Loops

In the transformed grammar, tail-recursive rules like:
$$\text{ColumnListTail} \longrightarrow , \text{ IDENTIFIER ColumnListTail} \mid \varepsilon$$
$$\text{OrExprTail} \longrightarrow \text{OR } \text{AndExpr } \text{OrExprTail} \mid \varepsilon$$

are implemented inside Python functions using a standard `while self._match(...)` loop rather than actual recursive function calls.

### Benefits of Iterative Parsing for Tail Rules:
1. **Zero Stack Overhead:** Avoids unnecessary call-frame allocations in Python.
2. **Linear Processing Time:** Tokens are consumed in $O(n)$ time directly proportional to query length.
3. **Clean Tree Building:** Allows appending siblings directly to parent nodes without creating deeply skewed, degenerate unary CST branches.

---

## 4. Clause Order Invariance and Enforcement

The grammar start production strictly specifies:
$$\text{Query} \longrightarrow \text{SelectClause FromClause WhereClauseOpt OrderByClauseOpt SemicolonOpt}$$

This enforces that:
1. `SELECT` is mandatory and must appear first.
2. `FROM` is mandatory and must directly follow the selection list.
3. `WHERE` is optional, but if present, must follow `FROM`.
4. `ORDER BY` is optional, but if present, must follow `WHERE` (or `FROM` if `WHERE` is absent).
5. If a `WHERE` keyword is encountered after `ORDER BY`, the parser flags an immediate `SyntaxError` with the exact line and column coordinates.
