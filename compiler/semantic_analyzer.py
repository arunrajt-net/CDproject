"""
Semantic Analyzer for the Mini SQL Compiler.
Validates table existence, column resolution, and data-type compatibility against the Symbol Table schema.
"""

from typing import List, Dict, Any, Optional
from .ast_nodes import (
    QueryNode,
    SelectClauseNode,
    FromClauseNode,
    WhereClauseNode,
    OrderByClauseNode,
    BinaryOpNode,
    UnaryOpNode,
    IdentifierNode,
    LiteralNode,
    WildcardNode,
    ASTNode,
)
from .symbol_table import SymbolTable
from .errors import SemanticError


class SemanticAnalyzer:
    """
    Semantic Analysis phase of the Mini SQL Compiler.
    Verifies:
      1. Table existence against the symbol table schema.
      2. Column presence in SELECT clause.
      3. Column presence in WHERE clause.
      4. Column presence in ORDER BY clause.
      5. Type compatibility in comparison expressions (INT/FLOAT vs VARCHAR).
    """

    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table: SymbolTable = symbol_table
        self.verified_items: List[Dict[str, str]] = []

    def analyze(self, ast: QueryNode) -> Dict[str, Any]:
        """
        Executes semantic checks on the AST.
        Raises SemanticError on semantic violations.
        Returns a dictionary of semantic analysis metrics and verification log.
        """
        self.verified_items = []

        # 1. Validate Table Existence
        table_name = ast.from_clause.table_name
        if not self.symbol_table.has_table(table_name):
            suggested = self.symbol_table.suggest_table(table_name)
            available = list(self.symbol_table.tables.keys())
            sugg_text = f"Did you mean '{suggested}'?" if suggested else f"Available tables: {', '.join(available)}"
            raise SemanticError(
                message=f"Table '{table_name}' does not exist in database schema",
                line=ast.from_clause.line,
                column=ast.from_clause.column,
                suggestion=sugg_text
            )

        self.verified_items.append({
            "check": "Table Existence",
            "target": table_name,
            "status": "PASSED",
            "detail": f"Table '{table_name}' successfully resolved in schema"
        })

        # 2. Validate SELECT Columns
        table_sym = self.symbol_table.get_table(table_name)
        available_cols = list(table_sym.columns.keys()) if table_sym else []

        for col_node in ast.select_clause.columns:
            if isinstance(col_node, WildcardNode):
                self.verified_items.append({
                    "check": "Column Resolution",
                    "target": "*",
                    "status": "PASSED",
                    "detail": f"Wildcard expanded to all columns in '{table_name}': ({', '.join(available_cols)})"
                })
            elif isinstance(col_node, IdentifierNode):
                col_name = col_node.name
                if not self.symbol_table.has_column(table_name, col_name):
                    suggested = self.symbol_table.suggest_column(table_name, col_name)
                    sugg_text = f"Did you mean '{suggested}'?" if suggested else f"Available columns in '{table_name}': {', '.join(available_cols)}"
                    raise SemanticError(
                        message=f"Column '{col_name}' does not exist in table '{table_name}'",
                        line=col_node.line,
                        column=col_node.column,
                        suggestion=sugg_text
                    )
                col_sym = self.symbol_table.get_column(table_name, col_name)
                self.verified_items.append({
                    "check": "Column Resolution",
                    "target": f"{table_name}.{col_name}",
                    "status": "PASSED",
                    "detail": f"Column '{col_name}' resolved to type {col_sym.data_type}"
                })

        # 3. Validate WHERE Clause Conditions
        if ast.where_clause:
            self._validate_condition(ast.where_clause.condition, table_name, available_cols)

        # 4. Validate ORDER BY Clause Columns
        if ast.order_by_clause:
            for item in ast.order_by_clause.items:
                col_name = item.column_name
                if not self.symbol_table.has_column(table_name, col_name):
                    suggested = self.symbol_table.suggest_column(table_name, col_name)
                    sugg_text = f"Did you mean '{suggested}'?" if suggested else f"Available columns in '{table_name}': {', '.join(available_cols)}"
                    raise SemanticError(
                        message=f"Column '{col_name}' in ORDER BY clause does not exist in table '{table_name}'",
                        line=item.line,
                        column=item.column,
                        suggestion=sugg_text
                    )
                col_sym = self.symbol_table.get_column(table_name, col_name)
                self.verified_items.append({
                    "check": "Order By Resolution",
                    "target": f"{table_name}.{col_name}",
                    "status": "PASSED",
                    "detail": f"Order column '{col_name}' resolved to type {col_sym.data_type} with sort direction {item.direction}"
                })

        return {
            "status": "PASSED",
            "table": table_name,
            "checks_count": len(self.verified_items),
            "verifications": self.verified_items,
        }

    def _validate_condition(self, node: ASTNode, table_name: str, available_cols: List[str]) -> None:
        if isinstance(node, BinaryOpNode):
            if node.operator in ("AND", "OR"):
                self._validate_condition(node.left, table_name, available_cols)
                self._validate_condition(node.right, table_name, available_cols)
            else:
                # Comparison operator (=, !=, <>, >, <, >=, <=)
                left_type = self._resolve_expr_type(node.left, table_name, available_cols)
                right_type = self._resolve_expr_type(node.right, table_name, available_cols)

                # Type compatibility check
                self._check_type_compatibility(left_type, right_type, node)
                self.verified_items.append({
                    "check": "Type Compatibility",
                    "target": f"{node.operator}",
                    "status": "PASSED",
                    "detail": f"Compared {left_type} with {right_type} successfully"
                })

        elif isinstance(node, UnaryOpNode):
            self._validate_condition(node.operand, table_name, available_cols)

    def _resolve_expr_type(self, node: ASTNode, table_name: str, available_cols: List[str]) -> str:
        if isinstance(node, IdentifierNode):
            col_name = node.name
            if not self.symbol_table.has_column(table_name, col_name):
                suggested = self.symbol_table.suggest_column(table_name, col_name)
                sugg_text = f"Did you mean '{suggested}'?" if suggested else f"Available columns in '{table_name}': {', '.join(available_cols)}"
                raise SemanticError(
                    message=f"Column '{col_name}' in WHERE clause does not exist in table '{table_name}'",
                    line=node.line,
                    column=node.column,
                    suggestion=sugg_text
                )
            col_sym = self.symbol_table.get_column(table_name, col_name)
            return col_sym.data_type

        if isinstance(node, LiteralNode):
            return node.literal_type

        return "UNKNOWN"

    def _check_type_compatibility(self, left_type: str, right_type: str, node: BinaryOpNode) -> None:
        numeric_types = {"INT", "FLOAT"}

        # Case 1: Numeric vs VARCHAR
        if (left_type in numeric_types and right_type == "VARCHAR") or (left_type == "VARCHAR" and right_type in numeric_types):
            left_desc = getattr(node.left, "name", None) or getattr(node.left, "value", "expression")
            right_desc = getattr(node.right, "name", None) or getattr(node.right, "value", "expression")
            raise SemanticError(
                message=f"Type mismatch in condition: cannot compare {left_type} ('{left_desc}') with {right_type} ('{right_desc}') using operator '{node.operator}'",
                line=node.line,
                column=node.column,
                suggestion=f"Convert the operand to match compatible data type ({left_type})"
            )
