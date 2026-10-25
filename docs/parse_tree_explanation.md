# Parse Tree and Abstract Syntax Tree (AST)

## 1. Concrete Syntax Tree (Parse Tree) vs. Abstract Syntax Tree (AST)

One of the central requirements of a compiler front-end is distinguishing between the **Concrete Syntax Tree (CST)** and the **Abstract Syntax Tree (AST)**:

| Feature | Concrete Syntax Tree (Parse Tree) | Abstract Syntax Tree (AST) |
|---|---|---|
| **Definition** | Direct graphical representation of the formal grammar derivation steps. | Condensed semantic representation of the query syntax. |
| **Syntactic Sugar** | Retains all punctuation tokens (commas, semicolons, parentheses). | Discards punctuation; only retains operative nodes and operands. |
| **Punctuation Keywords** | Explicitly models structural keywords (`FROM`, `ORDER BY`). | Encapsulates keywords into typed object structures (`FromClause`, `OrderByClause`). |
| **Purpose** | Syntax validation, debugging grammar rules, and formal derivation proofs. | Semantic analysis, type checking, query optimization, and execution planning. |

---

## 2. Dynamic Parse Tree Generation (`compiler/parse_tree.py`)

Each node in the CST is represented by a `ParseTreeNode` object containing:
- `name`: Non-terminal or terminal rule name (e.g. `Query`, `SELECT`, `SelectList`, `Condition`).
- `value`: Optional lexeme string (e.g. `students`, `age`, `>`, `18`).
- `line` & `column`: Source coordinate locations for pinpoint diagnostics.
- `children`: An ordered list of child `ParseTreeNode` instances.

### Sample Query:
```sql
SELECT name, age FROM students WHERE age > 18 ORDER BY age DESC;
```

### Generated Concrete Parse Tree (CST):
```
Query
├── SELECT ('SELECT')
│   └── SelectList
│       ├── Identifier ('name')
│       └── Identifier ('age')
├── FROM ('FROM')
│   └── Table ('students')
├── WHERE ('WHERE')
│   └── Condition ('>')
│       ├── Identifier ('age')
│       └── Number ('18')
├── ORDER BY ('ORDER BY')
│   └── OrderItem ('age DESC')
│       ├── Column ('age')
│       └── Direction ('DESC')
└── Semicolon (';')
```

---

## 3. Abstract Syntax Tree Representation (`compiler/ast_nodes.py`)

The AST strips away grammatical filler and directly organizes the query into an object hierarchy:
- `QueryNode`
  - `SelectClauseNode` (`distinct=False`, `columns=[IdentifierNode('name'), IdentifierNode('age')]`)
  - `FromClauseNode` (`table_name='students'`)
  - `WhereClauseNode` (`condition=BinaryOpNode(left='age', op='>', right=18)`)
  - `OrderByClauseNode` (`items=[OrderItemNode(col='age', dir='DESC')]`)

### Generated AST JSON Representation:
```json
{
  "node_type": "Query",
  "select": {
    "node_type": "SelectClause",
    "distinct": false,
    "columns": [
      { "node_type": "Identifier", "name": "name", "line": 1, "column": 8 },
      { "node_type": "Identifier", "name": "age", "line": 1, "column": 14 }
    ]
  },
  "from": {
    "node_type": "FromClause",
    "table_name": "students",
    "line": 1, "column": 23
  },
  "where": {
    "node_type": "WhereClause",
    "condition": {
      "node_type": "BinaryOp",
      "operator": ">",
      "left": { "node_type": "Identifier", "name": "age", "line": 1, "column": 38 },
      "right": { "node_type": "Literal", "data_type": "INT", "value": 18, "line": 1, "column": 44 }
    }
  },
  "order_by": {
    "node_type": "OrderByClause",
    "items": [
      { "node_type": "OrderItem", "column": "age", "direction": "DESC", "line": 1, "column": 56 }
    ]
  }
}
```
