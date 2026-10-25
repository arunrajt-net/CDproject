# Original Context-Free Grammar (Pre-Transformation)

## 1. Introduction
The natural grammar for SQL projection, list separation, and binary boolean operators is naturally expressed using **left-recursive productions**. However, top-down predictive parsers, including **Recursive Descent Parsers**, cannot directly parse left-recursive grammars without encountering infinite recursion.

---

## 2. Original Production Rules

```bnf
Query              ::= SelectClause FromClause WhereClauseOpt OrderByClauseOpt SemicolonOpt

SelectClause       ::= SELECT DistinctOpt SelectList
DistinctOpt        ::= DISTINCT | ε

SelectList         ::= * | ColumnList

/* Left-Recursive: ColumnList */
ColumnList         ::= ColumnList , IDENTIFIER
                     | IDENTIFIER

FromClause         ::= FROM IDENTIFIER TableAliasOpt
TableAliasOpt      ::= IDENTIFIER | ε

WhereClauseOpt     ::= WHERE Condition | ε

/* Left-Recursive: Boolean Expressions */
Condition          ::= OrExpr

OrExpr             ::= OrExpr OR AndExpr
                     | AndExpr

AndExpr            ::= AndExpr AND NotExpr
                     | NotExpr

NotExpr            ::= NOT NotExpr
                     | PrimaryCond

PrimaryCond        ::= ( Condition )
                     | CompExpr

CompExpr           ::= Operand COMP_OP Operand
Operand            ::= IDENTIFIER | NUMBER | STRING

/* Left-Recursive: OrderList */
OrderByClauseOpt   ::= ORDER BY OrderList | ε

OrderList          ::= OrderList , OrderItem
                     | OrderItem

OrderItem          ::= IDENTIFIER DirectionOpt
DirectionOpt       ::= ASC | DESC | ε

SemicolonOpt       ::= ; | ε
```

---

## 3. Left-Recursive Productions Identified

The following non-terminals contain immediate left recursion:

1. **`ColumnList`**:
   $$\text{ColumnList} \longrightarrow \text{ColumnList} , \text{IDENTIFIER} \mid \text{IDENTIFIER}$$
2. **`OrExpr`**:
   $$\text{OrExpr} \longrightarrow \text{OrExpr} \text{ OR } \text{AndExpr} \mid \text{AndExpr}$$
3. **`AndExpr`**:
   $$\text{AndExpr} \longrightarrow \text{AndExpr} \text{ AND } \text{NotExpr} \mid \text{NotExpr}$$
4. **`OrderList`**:
   $$\text{OrderList} \longrightarrow \text{OrderList} , \text{OrderItem} \mid \text{OrderItem}$$

### Why Left Recursion Must Be Eliminated:
In recursive descent parsing, each non-terminal corresponds directly to a Python parsing function. If `ColumnList()` immediately calls `ColumnList()` as its very first step before consuming any token from the input stream, the function invokes itself indefinitely:
$$\text{ColumnList}() \longrightarrow \text{ColumnList}() \longrightarrow \text{ColumnList}() \dots \longrightarrow \text{RecursionError: maximum recursion depth exceeded}$$

Therefore, formal grammar transformation is required to make the CFG LL(1) compatible.
