"""
Automated unit tests for Parse Tree and AST generation.
Verifies hierarchical parent-child relationships, text rendering, and JSON serialization.
"""

import unittest
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.parse_tree import ParseTreeNode


class TestParseTree(unittest.TestCase):

    def setUp(self):
        self.sql = "SELECT name, age FROM students WHERE age > 18 ORDER BY age DESC;"
        lexer = Lexer(self.sql)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        self.cst, self.ast = parser.parse()

    def test_cst_root_and_major_clauses(self):
        self.assertEqual(self.cst.name, "Query")
        clause_names = [child.name for child in self.cst.children]
        self.assertIn("SELECT", clause_names)
        self.assertIn("FROM", clause_names)
        self.assertIn("WHERE", clause_names)
        self.assertIn("ORDER BY", clause_names)
        self.assertIn("Semicolon", clause_names)

    def test_cst_child_hierarchy(self):
        # Locate SELECT node
        select_node = next(child for child in self.cst.children if child.name == "SELECT")
        list_node = next(child for child in select_node.children if child.name == "SelectList")
        identifiers = [child.value for child in list_node.children if child.name == "Identifier"]
        self.assertEqual(identifiers, ["name", "age"])

    def test_cst_json_serialization(self):
        tree_dict = self.cst.to_dict()
        self.assertIsInstance(tree_dict, dict)
        self.assertEqual(tree_dict["name"], "Query")
        self.assertTrue("children" in tree_dict)
        self.assertGreater(len(tree_dict["children"]), 0)

    def test_cst_text_rendering(self):
        text_tree = self.cst.to_text_tree(use_ascii=True)
        self.assertIn("Query", text_tree)
        self.assertIn("SELECT", text_tree)
        self.assertIn("FROM", text_tree)
        self.assertIn("WHERE", text_tree)
        self.assertIn("ORDER BY", text_tree)

    def test_ast_structure_and_json(self):
        ast_dict = self.ast.to_dict()
        self.assertEqual(ast_dict["node_type"], "Query")
        self.assertIn("select", ast_dict)
        self.assertIn("from", ast_dict)
        self.assertIn("where", ast_dict)
        self.assertIn("order_by", ast_dict)
        self.assertEqual(ast_dict["from"]["table_name"], "students")


if __name__ == "__main__":
    unittest.main()
