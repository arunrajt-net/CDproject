"""
Abstract Syntax Tree (AST) node definitions for the Mini SQL Compiler.
Unlike the Concrete Syntax Tree (Parse Tree), AST excludes concrete grammar tokens
such as commas, semicolons, and structural grouping tokens.
"""

from typing import List, Optional, Any, Dict


class ASTNode:
    """Base class for all Abstract Syntax Tree nodes."""
    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError

    def to_text_tree(self, prefix: str = "", is_last: bool = True, use_ascii: bool = False) -> str:
        d = self.to_dict()
        node_name = d.get("node_type", self.__class__.__name__)
        label = node_name
        extra = []
        for k, v in d.items():
            if k not in ("node_type", "children") and not isinstance(v, (list, dict)):
                extra.append(f"{k}={v}")
        if extra:
            label += f" ({', '.join(extra)})"

        c_last = "\\-- " if use_ascii else "└── "
        c_mid = "+-- " if use_ascii else "├── "
        p_pipe = "|   " if use_ascii else "│   "

        if not prefix:
            res = label + "\n"
        else:
            connector = c_last if is_last else c_mid
            res = prefix + connector + label + "\n"

        child_prefix = prefix + ("    " if is_last else p_pipe)
        children = []
        for k, v in d.items():
            if isinstance(v, list):
                for item in v:
                    if isinstance(item, dict) and "node_type" in item:
                        children.append(item)
            elif isinstance(v, dict) and "node_type" in v:
                children.append(v)

        for i, ch in enumerate(children):
            res += _dict_to_text_tree(ch, child_prefix, i == len(children) - 1, use_ascii=use_ascii)
        return res


def _dict_to_text_tree(d: Dict[str, Any], prefix: str = "", is_last: bool = True, use_ascii: bool = False) -> str:
    node_name = d.get("node_type", "Node")
    extra = []
    for k, v in d.items():
        if k not in ("node_type", "children") and not isinstance(v, (list, dict)):
            extra.append(f"{k}={v}")
    label = node_name
    if extra:
        label += f" ({', '.join(extra)})"

    c_last = "\\-- " if use_ascii else "└── "
    c_mid = "+-- " if use_ascii else "├── "
    p_pipe = "|   " if use_ascii else "│   "

    connector = c_last if is_last else c_mid
    res = prefix + connector + label + "\n"
    child_prefix = prefix + ("    " if is_last else p_pipe)

    children = []
    for k, v in d.items():
        if isinstance(v, list):
            for item in v:
                if isinstance(item, dict) and "node_type" in item:
                    children.append(item)
        elif isinstance(v, dict) and "node_type" in v:
            children.append(v)

    for i, ch in enumerate(children):
        res += _dict_to_text_tree(ch, child_prefix, i == len(children) - 1, use_ascii=use_ascii)
    return res


class IdentifierNode(ASTNode):
    def __init__(self, name: str, line: int = 1, column: int = 1):
        self.name = name
        self.line = line
        self.column = column

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_type": "Identifier",
            "name": self.name,
            "line": self.line,
            "column": self.column,
        }


class WildcardNode(ASTNode):
    def __init__(self, line: int = 1, column: int = 1):
        self.line = line
        self.column = column

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_type": "Wildcard",
            "value": "*",
            "line": self.line,
            "column": self.column,
        }


class LiteralNode(ASTNode):
    def __init__(self, value: Any, literal_type: str, line: int = 1, column: int = 1):
        self.value = value
        self.literal_type = literal_type
        self.line = line
        self.column = column

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_type": "Literal",
            "value": self.value,
            "data_type": self.literal_type,
            "line": self.line,
            "column": self.column,
        }


class BinaryOpNode(ASTNode):
    def __init__(self, left: Any, operator: str, right: Any, line: int = 1, column: int = 1):
        self.left = left
        self.operator = operator
        self.right = right
        self.line = line
        self.column = column

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_type": "BinaryOp",
            "operator": self.operator,
            "left": self.left.to_dict() if hasattr(self.left, "to_dict") else self.left,
            "right": self.right.to_dict() if hasattr(self.right, "to_dict") else self.right,
            "line": self.line,
            "column": self.column,
        }


class UnaryOpNode(ASTNode):
    def __init__(self, operator: str, operand: Any, line: int = 1, column: int = 1):
        self.operator = operator
        self.operand = operand
        self.line = line
        self.column = column

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_type": "UnaryOp",
            "operator": self.operator,
            "operand": self.operand.to_dict() if hasattr(self.operand, "to_dict") else self.operand,
            "line": self.line,
            "column": self.column,
        }


class SelectClauseNode(ASTNode):
    def __init__(self, is_distinct: bool, columns: List[Any]):
        self.is_distinct = is_distinct
        self.columns = columns

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_type": "SelectClause",
            "distinct": self.is_distinct,
            "columns": [col.to_dict() if hasattr(col, "to_dict") else col for col in self.columns],
        }


class FromClauseNode(ASTNode):
    def __init__(self, table_name: str, alias: Optional[str] = None, line: int = 1, column: int = 1):
        self.table_name = table_name
        self.alias = alias
        self.line = line
        self.column = column

    def to_dict(self) -> Dict[str, Any]:
        res = {
            "node_type": "FromClause",
            "table_name": self.table_name,
            "line": self.line,
            "column": self.column,
        }
        if self.alias:
            res["alias"] = self.alias
        return res


class WhereClauseNode(ASTNode):
    def __init__(self, condition: Any):
        self.condition = condition

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_type": "WhereClause",
            "condition": self.condition.to_dict() if hasattr(self.condition, "to_dict") else self.condition,
        }


class OrderItemNode(ASTNode):
    def __init__(self, column_name: str, direction: str = "ASC", line: int = 1, column: int = 1):
        self.column_name = column_name
        self.direction = direction.upper()
        self.line = line
        self.column = column

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_type": "OrderItem",
            "column": self.column_name,
            "direction": self.direction,
            "line": self.line,
            "column": self.column,
        }


class OrderByClauseNode(ASTNode):
    def __init__(self, items: List[OrderItemNode]):
        self.items = items

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_type": "OrderByClause",
            "items": [item.to_dict() for item in self.items],
        }


class QueryNode(ASTNode):
    def __init__(
        self,
        select_clause: SelectClauseNode,
        from_clause: FromClauseNode,
        where_clause: Optional[WhereClauseNode] = None,
        order_by_clause: Optional[OrderByClauseNode] = None
    ):
        self.select_clause = select_clause
        self.from_clause = from_clause
        self.where_clause = where_clause
        self.order_by_clause = order_by_clause

    def to_dict(self) -> Dict[str, Any]:
        res = {
            "node_type": "Query",
            "select": self.select_clause.to_dict(),
            "from": self.from_clause.to_dict(),
        }
        if self.where_clause:
            res["where"] = self.where_clause.to_dict()
        if self.order_by_clause:
            res["order_by"] = self.order_by_clause.to_dict()
        return res
