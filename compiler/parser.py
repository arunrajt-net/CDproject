"""
Recursive Descent Parser for the Mini SQL Compiler.
Implements syntax analysis for restricted SQL based on a transformed, non-left-recursive CFG.
Constructs both a Concrete Parse Tree (CST) and an Abstract Syntax Tree (AST).
"""

from typing import List, Tuple, Optional
from .tokens import Token, TokenType
from .errors import SyntaxError
from .parse_tree import ParseTreeNode
from .ast_nodes import (
    QueryNode,
    SelectClauseNode,
    FromClauseNode,
    WhereClauseNode,
    OrderByClauseNode,
    OrderItemNode,
    BinaryOpNode,
    UnaryOpNode,
    IdentifierNode,
    LiteralNode,
    WildcardNode,
    ASTNode,
)


class Parser:
    """
    Recursive Descent Syntax Analyzer.
    Validates token stream against grammar and enforces SQL clause order:
    SELECT -> FROM -> [WHERE] -> [ORDER BY] -> [;]
    """

    def __init__(self, tokens: List[Token]):
        self.tokens: List[Token] = tokens
        self.pos: int = 0

    # --------------------------------------------------------------------------
    # Token Navigation & Helper Utilities
    # --------------------------------------------------------------------------

    def _peek(self, offset: int = 0) -> Token:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]  # Return EOF

    def _previous(self) -> Token:
        return self.tokens[self.pos - 1]

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _check(self, token_type: TokenType, value: Optional[str] = None) -> bool:
        if self._is_at_end() and token_type != TokenType.EOF:
            return False
        curr = self._peek()
        if curr.type != token_type:
            return False
        if value is not None:
            if curr.literal_value is not None and isinstance(curr.literal_value, str):
                return curr.literal_value.upper() == value.upper()
            return curr.value.upper() == value.upper()
        return True

    def _match(self, token_type: TokenType, value: Optional[str] = None) -> bool:
        if self._check(token_type, value):
            self._advance()
            return True
        return False

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.pos += 1
        return self._previous()

    def _consume(
        self,
        token_type: TokenType,
        value: Optional[str] = None,
        error_msg: Optional[str] = None,
        suggestion: Optional[str] = None
    ) -> Token:
        if self._check(token_type, value):
            return self._advance()

        curr = self._peek()
        expected = value if value else token_type.value
        got = f"'{curr.value}'" if curr.value else "end of input"
        msg = error_msg or f"Expected {expected}, but found {got}"
        raise SyntaxError(
            message=msg,
            line=curr.line,
            column=curr.column,
            suggestion=suggestion
        )

    # --------------------------------------------------------------------------
    # Main Parsing Entry Point
    # --------------------------------------------------------------------------

    def parse(self) -> Tuple[ParseTreeNode, QueryNode]:
        """
        Parses the token stream and returns (ParseTreeNode, QueryNode).
        Raises SyntaxError upon syntax violations.
        """
        if self._is_at_end() or (len(self.tokens) == 1 and self.tokens[0].type == TokenType.EOF):
            raise SyntaxError(
                message="Empty query provided: SQL statement cannot be blank",
                line=1,
                column=1,
                suggestion="Enter a valid SQL query starting with SELECT"
            )

        parse_tree = ParseTreeNode(name="Query")

        # 1. SELECT clause (Mandatory)
        cst_select, ast_select = self._parse_select_clause()
        parse_tree.add_child(cst_select)

        # 2. FROM clause (Mandatory)
        cst_from, ast_from = self._parse_from_clause()
        parse_tree.add_child(cst_from)

        # 3. Optional WHERE clause
        ast_where: Optional[WhereClauseNode] = None
        if self._check(TokenType.KEYWORD, "WHERE"):
            cst_where, ast_where = self._parse_where_clause()
            parse_tree.add_child(cst_where)

        # 4. Optional ORDER BY clause
        ast_order: Optional[OrderByClauseNode] = None
        if self._check(TokenType.KEYWORD, "ORDER"):
            cst_order, ast_order = self._parse_order_by_clause()
            parse_tree.add_child(cst_order)

        # Check for invalid clause order (e.g., WHERE after ORDER BY)
        if self._check(TokenType.KEYWORD, "WHERE"):
            curr = self._peek()
            raise SyntaxError(
                message="WHERE clause cannot appear after ORDER BY clause",
                line=curr.line,
                column=curr.column,
                suggestion="Move the WHERE clause before the ORDER BY clause"
            )

        # 5. Optional Semicolon
        if self._match(TokenType.SEMICOLON):
            semi_tok = self._previous()
            cst_semi = ParseTreeNode(name="Semicolon", value=";", line=semi_tok.line, column=semi_tok.column)
            parse_tree.add_child(cst_semi)

        # 6. Ensure no extraneous tokens remain before EOF
        if not self._is_at_end():
            curr = self._peek()
            raise SyntaxError(
                message=f"Unexpected token '{curr.value}' found after query termination",
                line=curr.line,
                column=curr.column,
                suggestion="Remove trailing keywords or operators after the query"
            )

        ast_query = QueryNode(
            select_clause=ast_select,
            from_clause=ast_from,
            where_clause=ast_where,
            order_by_clause=ast_order
        )

        return parse_tree, ast_query

    # --------------------------------------------------------------------------
    # SELECT Clause Parsing
    # --------------------------------------------------------------------------

    def _parse_select_clause(self) -> Tuple[ParseTreeNode, SelectClauseNode]:
        curr = self._peek()
        if not self._check(TokenType.KEYWORD, "SELECT"):
            raise SyntaxError(
                message=f"Query must begin with 'SELECT' keyword, got '{curr.value}'",
                line=curr.line,
                column=curr.column,
                suggestion="Start your query with 'SELECT <columns> FROM <table>'"
            )

        sel_tok = self._advance()
        cst_select = ParseTreeNode(name="SELECT", value="SELECT", line=sel_tok.line, column=sel_tok.column)

        # Optional DISTINCT keyword
        is_distinct = False
        if self._check(TokenType.KEYWORD, "DISTINCT"):
            dist_tok = self._advance()
            cst_select.add_token_child("DISTINCT", "DISTINCT", dist_tok.line, dist_tok.column)
            is_distinct = True

        # Check for missing column list (e.g. SELECT FROM students)
        if self._check(TokenType.KEYWORD, "FROM"):
            curr = self._peek()
            raise SyntaxError(
                message="Missing column list or wildcard '*' in SELECT clause",
                line=curr.line,
                column=curr.column,
                suggestion="Specify columns (e.g., 'SELECT name, age' or 'SELECT *')"
            )

        cst_list = ParseTreeNode(name="SelectList")
        columns: List[ASTNode] = []

        # Wildcard '*' or Column List
        if self._match(TokenType.ASTERISK):
            ast_tok = self._previous()
            cst_list.add_token_child("Wildcard", "*", ast_tok.line, ast_tok.column)
            columns.append(WildcardNode(line=ast_tok.line, column=ast_tok.column))
        elif self._check(TokenType.IDENTIFIER):
            first_id = self._advance()
            cst_list.add_token_child("Identifier", first_id.value, first_id.line, first_id.column)
            columns.append(IdentifierNode(name=first_id.value, line=first_id.line, column=first_id.column))

            # Comma-separated columns: ColumnListTail -> , IDENTIFIER ColumnListTail | ε
            while self._match(TokenType.COMMA):
                comma_tok = self._previous()
                if self._check(TokenType.KEYWORD, "FROM"):
                    raise SyntaxError(
                        message="Trailing comma in SELECT column list with no following column identifier",
                        line=comma_tok.line,
                        column=comma_tok.column,
                        suggestion="Remove the trailing comma or add the next column name"
                    )
                next_id = self._consume(
                    TokenType.IDENTIFIER,
                    error_msg="Expected column identifier after comma in SELECT list",
                    suggestion="Provide a valid column name following the comma"
                )
                cst_list.add_token_child("Identifier", next_id.value, next_id.line, next_id.column)
                columns.append(IdentifierNode(name=next_id.value, line=next_id.line, column=next_id.column))
        else:
            curr = self._peek()
            raise SyntaxError(
                message=f"Invalid token '{curr.value}' in SELECT column list: expected column name or '*'",
                line=curr.line,
                column=curr.column,
                suggestion="Use column names or '*' to select all columns"
            )

        cst_select.add_child(cst_list)
        return cst_select, SelectClauseNode(is_distinct=is_distinct, columns=columns)

    # --------------------------------------------------------------------------
    # FROM Clause Parsing
    # --------------------------------------------------------------------------

    def _parse_from_clause(self) -> Tuple[ParseTreeNode, FromClauseNode]:
        curr = self._peek()
        if not self._check(TokenType.KEYWORD, "FROM"):
            raise SyntaxError(
                message=f"Expected 'FROM' keyword following SELECT clause, got '{curr.value}'",
                line=curr.line,
                column=curr.column,
                suggestion="Add 'FROM <table_name>' after the column list"
            )

        from_tok = self._advance()
        cst_from = ParseTreeNode(name="FROM", value="FROM", line=from_tok.line, column=from_tok.column)

        # Table identifier
        if self._is_at_end() or self._check(TokenType.SEMICOLON) or self._check(TokenType.KEYWORD):
            curr = self._peek()
            raise SyntaxError(
                message="Missing table name in FROM clause",
                line=curr.line,
                column=curr.column,
                suggestion="Specify a table name, e.g. 'FROM students'"
            )

        tbl_tok = self._consume(
            TokenType.IDENTIFIER,
            error_msg="Expected table name identifier after FROM",
            suggestion="Specify a valid table identifier (e.g. students, employees)"
        )
        cst_from.add_token_child("Table", tbl_tok.value, tbl_tok.line, tbl_tok.column)

        # Optional Table Alias
        alias: Optional[str] = None
        if self._check(TokenType.IDENTIFIER):
            # Next identifier is an alias (e.g. FROM students s)
            alias_tok = self._advance()
            cst_from.add_token_child("Alias", alias_tok.value, alias_tok.line, alias_tok.column)
            alias = alias_tok.value

        return cst_from, FromClauseNode(table_name=tbl_tok.value, alias=alias, line=tbl_tok.line, column=tbl_tok.column)

    # --------------------------------------------------------------------------
    # WHERE Clause Parsing
    # --------------------------------------------------------------------------

    def _parse_where_clause(self) -> Tuple[ParseTreeNode, WhereClauseNode]:
        where_tok = self._advance()  # Consume WHERE
        cst_where = ParseTreeNode(name="WHERE", value="WHERE", line=where_tok.line, column=where_tok.column)

        if self._is_at_end() or self._check(TokenType.SEMICOLON) or self._check(TokenType.KEYWORD, "ORDER"):
            curr = self._peek()
            raise SyntaxError(
                message="Missing search condition after WHERE keyword",
                line=curr.line,
                column=curr.column,
                suggestion="Provide a filtering condition, e.g. 'WHERE age > 18'"
            )

        cst_cond, ast_cond = self._parse_or_expr()
        cst_where.add_child(cst_cond)
        return cst_where, WhereClauseNode(condition=ast_cond)

    def _parse_or_expr(self) -> Tuple[ParseTreeNode, ASTNode]:
        cst_left, ast_left = self._parse_and_expr()

        while self._match(TokenType.KEYWORD, "OR"):
            op_tok = self._previous()
            if self._is_at_end() or self._check(TokenType.SEMICOLON):
                raise SyntaxError(
                    message="Missing expression following logical operator 'OR'",
                    line=op_tok.line,
                    column=op_tok.column,
                    suggestion="Add a condition after 'OR'"
                )
            cst_right, ast_right = self._parse_and_expr()

            cst_or = ParseTreeNode(name="LogicalExpr", value="OR", line=op_tok.line, column=op_tok.column)
            cst_or.add_child(cst_left)
            cst_or.add_child(cst_right)
            cst_left = cst_or
            ast_left = BinaryOpNode(
                left=ast_left,
                operator="OR",
                right=ast_right,
                line=op_tok.line,
                column=op_tok.column
            )

        return cst_left, ast_left

    def _parse_and_expr(self) -> Tuple[ParseTreeNode, ASTNode]:
        cst_left, ast_left = self._parse_not_expr()

        while self._match(TokenType.KEYWORD, "AND"):
            op_tok = self._previous()
            if self._is_at_end() or self._check(TokenType.SEMICOLON):
                raise SyntaxError(
                    message="Missing expression following logical operator 'AND'",
                    line=op_tok.line,
                    column=op_tok.column,
                    suggestion="Add a condition after 'AND'"
                )
            cst_right, ast_right = self._parse_not_expr()

            cst_and = ParseTreeNode(name="LogicalExpr", value="AND", line=op_tok.line, column=op_tok.column)
            cst_and.add_child(cst_left)
            cst_and.add_child(cst_right)
            cst_left = cst_and
            ast_left = BinaryOpNode(
                left=ast_left,
                operator="AND",
                right=ast_right,
                line=op_tok.line,
                column=op_tok.column
            )

        return cst_left, ast_left

    def _parse_not_expr(self) -> Tuple[ParseTreeNode, ASTNode]:
        if self._match(TokenType.KEYWORD, "NOT"):
            not_tok = self._previous()
            cst_sub, ast_sub = self._parse_not_expr()
            cst_not = ParseTreeNode(name="UnaryExpr", value="NOT", line=not_tok.line, column=not_tok.column)
            cst_not.add_child(cst_sub)
            ast_not = UnaryOpNode(operator="NOT", operand=ast_sub, line=not_tok.line, column=not_tok.column)
            return cst_not, ast_not

        return self._parse_primary_cond()

    def _parse_primary_cond(self) -> Tuple[ParseTreeNode, ASTNode]:
        if self._match(TokenType.LPAREN):
            lparen_tok = self._previous()
            cst_sub, ast_sub = self._parse_or_expr()
            rparen = self._consume(
                TokenType.RPAREN,
                error_msg="Unclosed parenthesis in condition: expected ')'",
                suggestion="Add a matching closing parenthesis ')'"
            )
            cst_group = ParseTreeNode(name="GroupedExpr", value="()", line=lparen_tok.line, column=lparen_tok.column)
            cst_group.add_child(cst_sub)
            return cst_group, ast_sub

        return self._parse_comp_expr()

    def _parse_comp_expr(self) -> Tuple[ParseTreeNode, BinaryOpNode]:
        cst_left, ast_left = self._parse_operand()

        curr = self._peek()
        if not self._check(TokenType.OPERATOR):
            raise SyntaxError(
                message=f"Expected comparison operator (=, !=, <>, >, <, >=, <=) after operand, found '{curr.value}'",
                line=curr.line,
                column=curr.column,
                suggestion="Include a valid comparison operator (e.g. =, >, <, >=, <=, !=)"
            )

        op_tok = self._advance()

        if self._is_at_end() or self._check(TokenType.SEMICOLON) or self._check(TokenType.KEYWORD):
            curr = self._peek()
            raise SyntaxError(
                message=f"Missing right-hand operand after comparison operator '{op_tok.value}'",
                line=curr.line,
                column=curr.column,
                suggestion="Provide a column, number, or string literal after the operator"
            )

        cst_right, ast_right = self._parse_operand()

        cst_comp = ParseTreeNode(name="Condition", value=op_tok.value, line=op_tok.line, column=op_tok.column)
        cst_comp.add_child(cst_left)
        cst_comp.add_child(cst_right)

        ast_comp = BinaryOpNode(
            left=ast_left,
            operator=op_tok.value,
            right=ast_right,
            line=op_tok.line,
            column=op_tok.column
        )
        return cst_comp, ast_comp

    def _parse_operand(self) -> Tuple[ParseTreeNode, ASTNode]:
        curr = self._peek()

        if self._match(TokenType.IDENTIFIER):
            tok = self._previous()
            cst = ParseTreeNode(name="Identifier", value=tok.value, line=tok.line, column=tok.column)
            ast = IdentifierNode(name=tok.value, line=tok.line, column=tok.column)
            return cst, ast

        if self._match(TokenType.NUMBER):
            tok = self._previous()
            dtype = "FLOAT" if isinstance(tok.literal_value, float) else "INT"
            cst = ParseTreeNode(name="Number", value=str(tok.value), line=tok.line, column=tok.column)
            ast = LiteralNode(value=tok.literal_value, literal_type=dtype, line=tok.line, column=tok.column)
            return cst, ast

        if self._match(TokenType.STRING):
            tok = self._previous()
            cst = ParseTreeNode(name="String", value=tok.value, line=tok.line, column=tok.column)
            ast = LiteralNode(value=tok.literal_value, literal_type="VARCHAR", line=tok.line, column=tok.column)
            return cst, ast

        raise SyntaxError(
            message=f"Expected column identifier, number, or string literal, but got '{curr.value}'",
            line=curr.line,
            column=curr.column,
            suggestion="Use a valid column name, integer, float, or 'string'"
        )

    # --------------------------------------------------------------------------
    # ORDER BY Clause Parsing
    # --------------------------------------------------------------------------

    def _parse_order_by_clause(self) -> Tuple[ParseTreeNode, OrderByClauseNode]:
        order_tok = self._advance()  # Consume ORDER
        self._consume(
            TokenType.KEYWORD,
            "BY",
            error_msg="Expected 'BY' keyword immediately following 'ORDER'",
            suggestion="Complete the clause with 'ORDER BY <columns>'"
        )

        cst_order = ParseTreeNode(name="ORDER BY", value="ORDER BY", line=order_tok.line, column=order_tok.column)

        if self._is_at_end() or self._check(TokenType.SEMICOLON):
            curr = self._peek()
            raise SyntaxError(
                message="Missing sorting column after ORDER BY keyword",
                line=curr.line,
                column=curr.column,
                suggestion="Specify at least one column to sort by (e.g. 'ORDER BY age DESC')"
            )

        items: List[OrderItemNode] = []
        cst_item, ast_item = self._parse_order_item()
        cst_order.add_child(cst_item)
        items.append(ast_item)

        while self._match(TokenType.COMMA):
            comma_tok = self._previous()
            if self._is_at_end() or self._check(TokenType.SEMICOLON):
                raise SyntaxError(
                    message="Trailing comma in ORDER BY list with no subsequent column specified",
                    line=comma_tok.line,
                    column=comma_tok.column,
                    suggestion="Remove the trailing comma or add another sorting column"
                )
            cst_next, ast_next = self._parse_order_item()
            cst_order.add_child(cst_next)
            items.append(ast_next)

        return cst_order, OrderByClauseNode(items=items)

    def _parse_order_item(self) -> Tuple[ParseTreeNode, OrderItemNode]:
        col_tok = self._consume(
            TokenType.IDENTIFIER,
            error_msg="Expected column name for ordering in ORDER BY clause",
            suggestion="Provide a valid column name to order by"
        )
        direction = "ASC"

        if self._check(TokenType.KEYWORD, "ASC"):
            self._advance()
            direction = "ASC"
        elif self._check(TokenType.KEYWORD, "DESC"):
            self._advance()
            direction = "DESC"

        cst_item = ParseTreeNode(
            name="OrderItem",
            value=f"{col_tok.value} {direction}",
            line=col_tok.line,
            column=col_tok.column
        )
        cst_item.add_token_child("Column", col_tok.value, col_tok.line, col_tok.column)
        cst_item.add_token_child("Direction", direction, col_tok.line, col_tok.column)

        ast_item = OrderItemNode(
            column_name=col_tok.value,
            direction=direction,
            line=col_tok.line,
            column=col_tok.column
        )
        return cst_item, ast_item
