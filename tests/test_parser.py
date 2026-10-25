"""
Automated unit tests for the Syntax Analyzer (Parser).
Validates CFG productions, operator precedence, clause order, and syntax error diagnostics.
"""

import unittest
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.errors import SyntaxError


class TestParser(unittest.TestCase):

    def _parse(self, sql: str):
        lexer = Lexer(sql)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        return parser.parse()

    def test_valid_select_wildcard(self):
        cst, ast = self._parse("SELECT * FROM students;")
        self.assertEqual(cst.name, "Query")
        self.assertEqual(ast.from_clause.table_name, "students")
        self.assertEqual(len(ast.select_clause.columns), 1)

    def test_valid_select_multiple_columns(self):
        cst, ast = self._parse("SELECT id, name, age, marks FROM students;")
        self.assertEqual(len(ast.select_clause.columns), 4)
        col_names = [col.name for col in ast.select_clause.columns]
        self.assertEqual(col_names, ["id", "name", "age", "marks"])

    def test_valid_distinct(self):
        cst, ast = self._parse("SELECT DISTINCT department FROM employees;")
        self.assertTrue(ast.select_clause.is_distinct)

    def test_valid_table_alias(self):
        cst, ast = self._parse("SELECT name FROM students s;")
        self.assertEqual(ast.from_clause.alias, "s")

    def test_valid_where_logical_precedence(self):
        query = "SELECT * FROM students WHERE (age > 18 OR marks > 80) AND department = 'CSE';"
        cst, ast = self._parse(query)
        self.assertIsNotNone(ast.where_clause)
        # Root of condition should be AND
        self.assertEqual(ast.where_clause.condition.operator, "AND")

    def test_valid_not_operator(self):
        query = "SELECT * FROM students WHERE NOT age < 18;"
        cst, ast = self._parse(query)
        self.assertEqual(ast.where_clause.condition.operator, "NOT")

    def test_valid_order_by_multiple_columns(self):
        query = "SELECT name, marks FROM students ORDER BY marks DESC, name ASC;"
        cst, ast = self._parse(query)
        self.assertIsNotNone(ast.order_by_clause)
        self.assertEqual(len(ast.order_by_clause.items), 2)
        self.assertEqual(ast.order_by_clause.items[0].column_name, "marks")
        self.assertEqual(ast.order_by_clause.items[0].direction, "DESC")
        self.assertEqual(ast.order_by_clause.items[1].column_name, "name")
        self.assertEqual(ast.order_by_clause.items[1].direction, "ASC")

    def test_syntax_error_missing_select(self):
        with self.assertRaises(SyntaxError) as ctx:
            self._parse("FROM students;")
        self.assertIn("Query must begin with 'SELECT'", ctx.exception.message)

    def test_syntax_error_missing_from(self):
        with self.assertRaises(SyntaxError) as ctx:
            self._parse("SELECT name students;")
        self.assertIn("Expected 'FROM' keyword", ctx.exception.message)

    def test_syntax_error_missing_table_name(self):
        with self.assertRaises(SyntaxError) as ctx:
            self._parse("SELECT name FROM;")
        self.assertIn("Missing table name in FROM clause", ctx.exception.message)

    def test_syntax_error_missing_selected_column(self):
        with self.assertRaises(SyntaxError) as ctx:
            self._parse("SELECT FROM students;")
        self.assertIn("Missing column list or wildcard", ctx.exception.message)

    def test_syntax_error_missing_where_condition(self):
        with self.assertRaises(SyntaxError) as ctx:
            self._parse("SELECT name FROM students WHERE;")
        self.assertIn("Missing search condition after WHERE", ctx.exception.message)

    def test_syntax_error_missing_order_by_column(self):
        with self.assertRaises(SyntaxError) as ctx:
            self._parse("SELECT name FROM students ORDER BY;")
        self.assertIn("Missing sorting column after ORDER BY", ctx.exception.message)

    def test_syntax_error_missing_comparison_operand(self):
        with self.assertRaises(SyntaxError) as ctx:
            self._parse("SELECT name FROM students WHERE age >; ")
        self.assertIn("Missing right-hand operand after comparison operator", ctx.exception.message)

    def test_syntax_error_trailing_comma(self):
        with self.assertRaises(SyntaxError) as ctx:
            self._parse("SELECT name, FROM students;")
        self.assertIn("Trailing comma in SELECT column list", ctx.exception.message)

    def test_syntax_error_clause_order_violation(self):
        with self.assertRaises(SyntaxError) as ctx:
            self._parse("SELECT name FROM students ORDER BY age WHERE age > 18;")
        self.assertIn("WHERE clause cannot appear after ORDER BY", ctx.exception.message)

    def test_syntax_error_trailing_tokens(self):
        with self.assertRaises(SyntaxError) as ctx:
            self._parse("SELECT name FROM students; unexpected_token")
        self.assertIn("Unexpected token 'unexpected_token'", ctx.exception.message)


if __name__ == "__main__":
    unittest.main()
