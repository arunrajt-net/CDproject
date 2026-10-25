# Transformed Context-Free Grammar (LL(1) Compatible)

## 1. Left-Recursion Elimination Technique

To eliminate direct left-recursion of the form:
$$A \longrightarrow A\alpha \mid \beta$$
(where $\beta$ does not begin with $A$), we introduce a new tail non-terminal $A'$:
$$A \longrightarrow \beta A'$$
$$A' \longrightarrow \alpha A' \mid \varepsilon$$

This replaces left recursion with right recursion, which a Recursive Descent Parser can process either recursively or iteratively using a `while` loop over token lookahead.

---

## 2. Derivation of Transformed Rules

### 2.1 Transformation of `ColumnList`
- **Original:** $\text{ColumnList} \longrightarrow \text{ColumnList} , \text{IDENTIFIER} \mid \text{IDENTIFIER}$
- Here, $A = \text{ColumnList}$, $\alpha = , \text{IDENTIFIER}$, $\beta = \text{IDENTIFIER}$
- **Transformed:**
  $$\text{ColumnList} \longrightarrow \text{IDENTIFIER } \text{ColumnListTail}$$
  $$\text{ColumnListTail} \longrightarrow , \text{IDENTIFIER } \text{ColumnListTail} \mid \varepsilon$$

### 2.2 Transformation of `OrExpr`
- **Original:** $\text{OrExpr} \longrightarrow \text{OrExpr} \text{ OR } \text{AndExpr} \mid \text{AndExpr}$
- Here, $A = \text{OrExpr}$, $\alpha = \text{OR } \text{AndExpr}$, $\beta = \text{AndExpr}$
- **Transformed:**
  $$\text{OrExpr} \longrightarrow \text{AndExpr } \text{OrExprTail}$$
  $$\text{OrExprTail} \longrightarrow \text{OR } \text{AndExpr } \text{OrExprTail} \mid \varepsilon$$

### 2.3 Transformation of `AndExpr`
- **Original:** $\text{AndExpr} \longrightarrow \text{AndExpr} \text{ AND } \text{NotExpr} \mid \text{NotExpr}$
- Here, $A = \text{AndExpr}$, $\alpha = \text{AND } \text{NotExpr}$, $\beta = \text{NotExpr}$
- **Transformed:**
  $$\text{AndExpr} \longrightarrow \text{NotExpr } \text{AndExprTail}$$
  $$\text{AndExprTail} \longrightarrow \text{AND } \text{NotExpr } \text{AndExprTail} \mid \varepsilon$$

### 2.4 Transformation of `OrderList`
- **Original:** $\text{OrderList} \longrightarrow \text{OrderList} , \text{OrderItem} \mid \text{OrderItem}$
- Here, $A = \text{OrderList}$, $\alpha = , \text{OrderItem}$, $\beta = \text{OrderItem}$
- **Transformed:**
  $$\text{OrderList} \longrightarrow \text{OrderItem } \text{OrderListTail}$$
  $$\text{OrderListTail} \longrightarrow , \text{OrderItem } \text{OrderListTail} \mid \varepsilon$$

---

## 3. Complete Transformed Grammar

```bnf
Query              ::= SelectClause FromClause WhereClauseOpt OrderByClauseOpt SemicolonOpt

SelectClause       ::= SELECT DistinctOpt SelectList
DistinctOpt        ::= DISTINCT | ε

SelectList         ::= * | ColumnList
ColumnList         ::= IDENTIFIER ColumnListTail
ColumnListTail     ::= , IDENTIFIER ColumnListTail | ε

FromClause         ::= FROM IDENTIFIER TableAliasOpt
TableAliasOpt      ::= IDENTIFIER | ε

WhereClauseOpt     ::= WHERE Condition | ε

Condition          ::= OrExpr
OrExpr             ::= AndExpr OrExprTail
OrExprTail         ::= OR AndExpr OrExprTail | ε

AndExpr            ::= NotExpr AndExprTail
AndExprTail        ::= AND NotExpr AndExprTail | ε

NotExpr            ::= NOT NotExpr | PrimaryCond
PrimaryCond        ::= ( Condition ) | CompExpr

CompExpr           ::= Operand COMP_OP Operand
Operand            ::= IDENTIFIER | NUMBER | STRING

OrderByClauseOpt   ::= ORDER BY OrderList | ε
OrderList          ::= OrderItem OrderListTail
OrderListTail      ::= , OrderItem OrderListTail | ε

OrderItem          ::= IDENTIFIER DirectionOpt
DirectionOpt       ::= ASC | DESC | ε

SemicolonOpt       ::= ; | ε
```

This transformed grammar is deterministic, free of left recursion, and aligns 1:1 with the implementation in `compiler/parser.py`.
