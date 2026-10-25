"""
Automated unit tests for Semantic Analyzer and Symbol Table.
Tests schema resolution, type compatibility, and diagnostic suggestions.
"""

import unittest
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.symbol_table import SymbolTable
from compiler.semantic_analyzer import SemanticAnalyzer
from compiler.errors import SemanticError


class TestSemantic(unittest.TestCase):

    def setUp(self):
        schema = {
            "students": {
                "columns": {
                    "id": {"type": "INT"},
                    "name": {"type": "VARCHAR"},
                    "age": {"type": "INT"},
                    "department": {"type": "VARCHAR"},
                    "marks": {"type": "FLOAT"}
                }
            },
            "employees": {
                "columns": {
                    "id": {"type": "INT"},
                    "name": {"type": "VARCHAR"},
                    "salary": {"type": "FLOAT"},
                    "department": {"type": "VARCHAR"}
                }
            }
        }
        self.sym_table = SymbolTable(schema)
        self.analyzer = SemanticAnalyzer(self.sym_table)

    def _analyze(self, sql: str):
        lexer = Lexer(sql)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        _, ast = parser.parse()
        return self.analyzer.analyze(ast)

    def test_valid_query_semantic(self):
        report = self._analyze("SELECT name, age FROM students WHERE age > 18 ORDER BY marks DESC;")
        self.assertEqual(report["status"], "PASSED")
        self.assertEqual(report["table"], "students")
        self.assertGreater(report["checks_count"], 0)

    def test_valid_wildcard_semantic(self):
        report = self._analyze("SELECT * FROM employees WHERE salary > 50000.0;")
        self.assertEqual(report["status"], "PASSED")

    def test_semantic_error_unknown_table(self):
        with self.assertRaises(SemanticError) as ctx:
            self._analyze("SELECT name FROM unknown_table;")
        self.assertIn("Table 'unknown_table' does not exist", ctx.exception.message)

    def test_semantic_error_unknown_select_column(self):
        with self.assertRaises(SemanticError) as ctx:
            self._analyze("SELECT salary FROM students;")
        self.assertIn("Column 'salary' does not exist in table 'students'", ctx.exception.message)

    def test_semantic_error_unknown_where_column(self):
        with self.assertRaises(SemanticError) as ctx:
            self._analyze("SELECT name FROM students WHERE gpa > 3.5;")
        self.assertIn("Column 'gpa' in WHERE clause does not exist", ctx.exception.message)

    def test_semantic_error_unknown_order_by_column(self):
        with self.assertRaises(SemanticError) as ctx:
            self._analyze("SELECT name FROM students ORDER BY ranking DESC;")
        self.assertIn("Column 'ranking' in ORDER BY clause does not exist", ctx.exception.message)

    def test_semantic_error_type_mismatch(self):
        with self.assertRaises(SemanticError) as ctx:
            self._analyze("SELECT name FROM students WHERE age = 'twenty';")
        self.assertIn("Type mismatch in condition", ctx.exception.message)


if __name__ == "__main__":
    unittest.main()
