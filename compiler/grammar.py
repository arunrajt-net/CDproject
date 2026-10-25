"""
Context-Free Grammar (CFG) definitions, production rules,
and FIRST / FOLLOW set metadata for the Mini SQL Compiler.
"""

from typing import Dict, List, Set


GRAMMAR_PRODUCTIONS = {
    "Query": [
        "SelectClause FromClause WhereClauseOpt OrderByClauseOpt SemicolonOpt"
    ],
    "SelectClause": [
        "SELECT DistinctOpt SelectList"
    ],
    "DistinctOpt": [
        "DISTINCT",
        "ε"
    ],
    "SelectList": [
        "*",
        "ColumnList"
    ],
    "ColumnList": [
        "IDENTIFIER ColumnListTail"
    ],
    "ColumnListTail": [
        ", IDENTIFIER ColumnListTail",
        "ε"
    ],
    "FromClause": [
        "FROM IDENTIFIER TableAliasOpt"
    ],
    "TableAliasOpt": [
        "IDENTIFIER",
        "ε"
    ],
    "WhereClauseOpt": [
        "WHERE Condition",
        "ε"
    ],
    "Condition": [
        "OrExpr"
    ],
    "OrExpr": [
        "AndExpr OrExprTail"
    ],
    "OrExprTail": [
        "OR AndExpr OrExprTail",
        "ε"
    ],
    "AndExpr": [
        "NotExpr AndExprTail"
    ],
    "AndExprTail": [
        "AND NotExpr AndExprTail",
        "ε"
    ],
    "NotExpr": [
        "NOT NotExpr",
        "PrimaryCond"
    ],
    "PrimaryCond": [
        "( Condition )",
        "CompExpr"
    ],
    "CompExpr": [
        "Operand COMP_OP Operand"
    ],
    "Operand": [
        "IDENTIFIER",
        "NUMBER",
        "STRING"
    ],
    "OrderByClauseOpt": [
        "ORDER BY OrderList",
        "ε"
    ],
    "OrderList": [
        "OrderItem OrderListTail"
    ],
    "OrderListTail": [
        ", OrderItem OrderListTail",
        "ε"
    ],
    "OrderItem": [
        "IDENTIFIER DirectionOpt"
    ],
    "DirectionOpt": [
        "ASC",
        "DESC",
        "ε"
    ],
    "SemicolonOpt": [
        ";",
        "ε"
    ]
}

FIRST_SETS: Dict[str, Set[str]] = {
    "Query": {"SELECT"},
    "SelectClause": {"SELECT"},
    "DistinctOpt": {"DISTINCT", "ε"},
    "SelectList": {"*", "IDENTIFIER"},
    "ColumnList": {"IDENTIFIER"},
    "ColumnListTail": {",", "ε"},
    "FromClause": {"FROM"},
    "TableAliasOpt": {"IDENTIFIER", "ε"},
    "WhereClauseOpt": {"WHERE", "ε"},
    "Condition": {"NOT", "(", "IDENTIFIER", "NUMBER", "STRING"},
    "OrExpr": {"NOT", "(", "IDENTIFIER", "NUMBER", "STRING"},
    "OrExprTail": {"OR", "ε"},
    "AndExpr": {"NOT", "(", "IDENTIFIER", "NUMBER", "STRING"},
    "AndExprTail": {"AND", "ε"},
    "NotExpr": {"NOT", "(", "IDENTIFIER", "NUMBER", "STRING"},
    "PrimaryCond": {"(", "IDENTIFIER", "NUMBER", "STRING"},
    "CompExpr": {"IDENTIFIER", "NUMBER", "STRING"},
    "Operand": {"IDENTIFIER", "NUMBER", "STRING"},
    "OrderByClauseOpt": {"ORDER", "ε"},
    "OrderList": {"IDENTIFIER"},
    "OrderListTail": {",", "ε"},
    "OrderItem": {"IDENTIFIER"},
    "DirectionOpt": {"ASC", "DESC", "ε"},
    "SemicolonOpt": {";", "ε"}
}

FOLLOW_SETS: Dict[str, Set[str]] = {
    "Query": {"$"},
    "SelectClause": {"FROM"},
    "DistinctOpt": {"*", "IDENTIFIER"},
    "SelectList": {"FROM"},
    "ColumnList": {"FROM"},
    "ColumnListTail": {"FROM"},
    "FromClause": {"WHERE", "ORDER", ";", "$"},
    "TableAliasOpt": {"WHERE", "ORDER", ";", "$"},
    "WhereClauseOpt": {"ORDER", ";", "$"},
    "Condition": {"ORDER", ";", "$", ")"},
    "OrExpr": {"ORDER", ";", "$", ")"},
    "OrExprTail": {"ORDER", ";", "$", ")"},
    "AndExpr": {"OR", "ORDER", ";", "$", ")"},
    "AndExprTail": {"OR", "ORDER", ";", "$", ")"},
    "NotExpr": {"AND", "OR", "ORDER", ";", "$", ")"},
    "PrimaryCond": {"AND", "OR", "ORDER", ";", "$", ")"},
    "CompExpr": {"AND", "OR", "ORDER", ";", "$", ")"},
    "Operand": {"COMP_OP", "AND", "OR", "ORDER", ";", "$", ")"},
    "OrderByClauseOpt": {";", "$"},
    "OrderList": {";", "$"},
    "OrderListTail": {";", "$"},
    "OrderItem": {",", ";", "$"},
    "DirectionOpt": {",", ";", "$"},
    "SemicolonOpt": {"$"}
}
