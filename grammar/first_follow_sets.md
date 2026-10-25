# FIRST and FOLLOW Sets

## 1. Mathematical Definitions

For a Context-Free Grammar $G = (V, \Sigma, R, S)$:

1. **$\text{FIRST}(\alpha)$**: The set of terminals that begin strings derived from $\alpha$. If $\alpha \xRightarrow{*} \varepsilon$, then $\varepsilon \in \text{FIRST}(\alpha)$.
2. **$\text{FOLLOW}(A)$**: The set of terminals that can appear immediately to the right of non-terminal $A$ in some sentential form. If $A$ is the start symbol, $\$$ (end of input) is in $\text{FOLLOW}(A)$.

---

## 2. Comprehensive FIRST and FOLLOW Table

| Non-Terminal | FIRST Set | FOLLOW Set |
|---|---|---|
| **`Query`** | `{ SELECT }` | `{ $ }` |
| **`SelectClause`** | `{ SELECT }` | `{ FROM }` |
| **`DistinctOpt`** | `{ DISTINCT, ε }` | `{ *, IDENTIFIER }` |
| **`SelectList`** | `{ *, IDENTIFIER }` | `{ FROM }` |
| **`ColumnList`** | `{ IDENTIFIER }` | `{ FROM }` |
| **`ColumnListTail`** | `{ ,, ε }` | `{ FROM }` |
| **`FromClause`** | `{ FROM }` | `{ WHERE, ORDER, ;, $ }` |
| **`TableAliasOpt`** | `{ IDENTIFIER, ε }` | `{ WHERE, ORDER, ;, $ }` |
| **`WhereClauseOpt`** | `{ WHERE, ε }` | `{ ORDER, ;, $ }` |
| **`Condition`** | `{ NOT, (, IDENTIFIER, NUMBER, STRING }` | `{ ORDER, ;, $, ) }` |
| **`OrExpr`** | `{ NOT, (, IDENTIFIER, NUMBER, STRING }` | `{ ORDER, ;, $, ) }` |
| **`OrExprTail`** | `{ OR, ε }` | `{ ORDER, ;, $, ) }` |
| **`AndExpr`** | `{ NOT, (, IDENTIFIER, NUMBER, STRING }` | `{ OR, ORDER, ;, $, ) }` |
| **`AndExprTail`** | `{ AND, ε }` | `{ OR, ORDER, ;, $, ) }` |
| **`NotExpr`** | `{ NOT, (, IDENTIFIER, NUMBER, STRING }` | `{ AND, OR, ORDER, ;, $, ) }` |
| **`PrimaryCond`** | `{ (, IDENTIFIER, NUMBER, STRING }` | `{ AND, OR, ORDER, ;, $, ) }` |
| **`CompExpr`** | `{ IDENTIFIER, NUMBER, STRING }` | `{ AND, OR, ORDER, ;, $, ) }` |
| **`Operand`** | `{ IDENTIFIER, NUMBER, STRING }` | `{ =, !=, <>, <, <=, >, >=, AND, OR, ORDER, ;, $, ) }` |
| **`OrderByClauseOpt`** | `{ ORDER, ε }` | `{ ;, $ }` |
| **`OrderList`** | `{ IDENTIFIER }` | `{ ;, $ }` |
| **`OrderListTail`** | `{ ,, ε }` | `{ ;, $ }` |
| **`OrderItem`** | `{ IDENTIFIER }` | `{ ,, ;, $ }` |
| **`DirectionOpt`** | `{ ASC, DESC, ε }` | `{ ,, ;, $ }` |
| **`SemicolonOpt`** | `{ ;, ε }` | `{ $ }` |

---

## 3. Verification of the LL(1) Condition

A grammar is LL(1) if and only if for every non-terminal $A$ with multiple productions $A \longrightarrow \alpha_1 \mid \alpha_2 \mid \dots \mid \alpha_n$:
1. $\text{FIRST}(\alpha_i) \cap \text{FIRST}(\alpha_j) = \emptyset$ for all $i \neq j$.
2. If $\alpha_i \xRightarrow{*} \varepsilon$, then $\text{FIRST}(\alpha_j) \cap \text{FOLLOW}(A) = \emptyset$ for all $j \neq i$.

### Example: `SelectList`
$$\text{SelectList} \longrightarrow * \mid \text{ColumnList}$$
- $\text{FIRST}(*) = \{ * \}$
- $\text{FIRST}(\text{ColumnList}) = \{ \text{IDENTIFIER} \}$
- $\{ * \} \cap \{ \text{IDENTIFIER} \} = \emptyset$ (Disjoint $\implies$ LL(1) valid)

### Example: `ColumnListTail`
$$\text{ColumnListTail} \longrightarrow , \text{ IDENTIFIER ColumnListTail} \mid \varepsilon$$
- $\text{FIRST}(, \dots) = \{ , \}$
- $\text{FOLLOW}(\text{ColumnListTail}) = \{ \text{FROM} \}$
- $\{ , \} \cap \{ \text{FROM} \} = \emptyset$ (Disjoint $\implies$ LL(1) valid)

This guarantees that the parser can deterministically decide which production rule to expand by inspecting only 1 token of lookahead ($k=1$).
