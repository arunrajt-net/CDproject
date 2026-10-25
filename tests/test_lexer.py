"""
Automated unit tests for the Lexical Analyzer (Lexer).
Tests token classification, line/col tracking, string escaping, comments, and lexical errors.
"""

import unittest
from compiler.lexer import Lexer
from compiler.tokens import TokenType
from compiler.errors import LexicalError


class TestLexer(unittest.TestCase):

    def test_keywords_case_insensitivity(self):
        query = "select DISTINCT FrOm WHERE order BY asc desc AND or NOT"
        lexer = Lexer(query)
        tokens = lexer.tokenize()

        expected = [
            "SELECT", "DISTINCT", "FROM", "WHERE", "ORDER",
            "BY", "ASC", "DESC", "AND", "OR", "NOT"
        ]
        for i, val in enumerate(expected):
            self.assertEqual(tokens[i].type, TokenType.KEYWORD)
            self.assertEqual(tokens[i].literal_value, val)

    def test_identifiers_and_numbers(self):
        query = "student_id 42 3.1415 salary_2026"
        lexer = Lexer(query)
        tokens = lexer.tokenize()

        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].value, "student_id")

        self.assertEqual(tokens[1].type, TokenType.NUMBER)
        self.assertEqual(tokens[1].literal_value, 42)

        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertAlmostEqual(tokens[2].literal_value, 3.1415)

        self.assertEqual(tokens[3].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[3].value, "salary_2026")

    def test_string_literals_and_escapes(self):
        query = "'Computer Science' 'It\\'s cool\\n'"
        lexer = Lexer(query)
        tokens = lexer.tokenize()

        self.assertEqual(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].literal_value, "Computer Science")

        self.assertEqual(tokens[1].type, TokenType.STRING)
        self.assertEqual(tokens[1].literal_value, "It's cool\n")

    def test_comparison_operators(self):
        query = "= != <> < <= > >="
        lexer = Lexer(query)
        tokens = lexer.tokenize()

        expected_ops = ["=", "!=", "<>", "<", "<=", ">", ">="]
        for i, op in enumerate(expected_ops):
            self.assertEqual(tokens[i].type, TokenType.OPERATOR)
            self.assertEqual(tokens[i].value, op)

    def test_delimiters_and_wildcard(self):
        query = "*,;()"
        lexer = Lexer(query)
        tokens = lexer.tokenize()

        self.assertEqual(tokens[0].type, TokenType.ASTERISK)
        self.assertEqual(tokens[1].type, TokenType.COMMA)
        self.assertEqual(tokens[2].type, TokenType.SEMICOLON)
        self.assertEqual(tokens[3].type, TokenType.LPAREN)
        self.assertEqual(tokens[4].type, TokenType.RPAREN)

    def test_line_and_column_tracking(self):
        query = "SELECT\n  name,\n  age"
        lexer = Lexer(query)
        tokens = lexer.tokenize()

        # SELECT at line 1, col 1
        self.assertEqual(tokens[0].line, 1)
        self.assertEqual(tokens[0].column, 1)

        # name at line 2, col 3
        self.assertEqual(tokens[1].line, 2)
        self.assertEqual(tokens[1].column, 3)

        # age at line 3, col 3
        self.assertEqual(tokens[3].line, 3)
        self.assertEqual(tokens[3].column, 3)

    def test_comments_skipping(self):
        query = "-- Single line comment\nSELECT name /* inline comment */ FROM students;"
        lexer = Lexer(query)
        tokens = lexer.tokenize()

        token_types = [t.type for t in tokens if t.type != TokenType.EOF]
        self.assertEqual(
            token_types,
            [TokenType.KEYWORD, TokenType.IDENTIFIER, TokenType.KEYWORD, TokenType.IDENTIFIER, TokenType.SEMICOLON]
        )

    def test_lexical_error_invalid_character(self):
        query = "SELECT name FROM students @;"
        lexer = Lexer(query)
        with self.assertRaises(LexicalError) as ctx:
            lexer.tokenize()
        self.assertIn("@", ctx.exception.message)
        self.assertEqual(ctx.exception.line, 1)
        self.assertEqual(ctx.exception.column, 27)

    def test_lexical_error_unterminated_string(self):
        query = "SELECT * FROM students WHERE name = 'John"
        lexer = Lexer(query)
        with self.assertRaises(LexicalError) as ctx:
            lexer.tokenize()
        self.assertIn("Unterminated string literal", ctx.exception.message)

    def test_lexical_error_invalid_number_prefix(self):
        query = "SELECT 123student FROM students;"
        lexer = Lexer(query)
        with self.assertRaises(LexicalError) as ctx:
            lexer.tokenize()
        self.assertIn("identifiers cannot start with numbers", ctx.exception.message)


if __name__ == "__main__":
    unittest.main()
