"""
Automated end-to-end integration tests for MiniSQLCompiler.
Executes all mandated valid and invalid queries from the project specification.
"""

import unittest
from compiler.compiler import MiniSQLCompiler


class TestCompilerIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.compiler = MiniSQLCompiler("schema/sample_schema.json")

    # --------------------------------------------------------------------------
    # Mandated Valid Test Cases (Part 13)
    # --------------------------------------------------------------------------

    def test_valid_01_wildcard_select(self):
        res = self.compiler.compile("SELECT * FROM students;")
        self.assertTrue(res.is_success)
        self.assertEqual(len(res.errors), 0)
        self.assertEqual(res.phases["lexical"], "PASSED")
        self.assertEqual(res.phases["syntax"], "PASSED")
        self.assertEqual(res.phases["semantic"], "PASSED")

    def test_valid_02_single_column_select(self):
        res = self.compiler.compile("SELECT name FROM students;")
        self.assertTrue(res.is_success)
        self.assertEqual(len(res.errors), 0)

    def test_valid_03_where_simple_numeric(self):
        res = self.compiler.compile("SELECT name, age FROM students WHERE age > 18;")
        self.assertTrue(res.is_success)
        self.assertEqual(len(res.errors), 0)

    def test_valid_04_order_by_desc(self):
        res = self.compiler.compile("SELECT name FROM students ORDER BY age DESC;")
        self.assertTrue(res.is_success)
        self.assertEqual(len(res.errors), 0)

    def test_valid_05_where_and_order_by(self):
        res = self.compiler.compile("SELECT name, marks FROM students WHERE marks >= 80 ORDER BY marks ASC;")
        self.assertTrue(res.is_success)
        self.assertEqual(len(res.errors), 0)

    def test_valid_06_where_compound_and(self):
        res = self.compiler.compile("SELECT name FROM students WHERE age > 18 AND department = 'CSE';")
        self.assertTrue(res.is_success)
        self.assertEqual(len(res.errors), 0)

    def test_valid_07_employees_table_numeric_salary(self):
        res = self.compiler.compile("SELECT name FROM employees WHERE salary > 30000;")
        self.assertTrue(res.is_success)
        self.assertEqual(len(res.errors), 0)

    def test_valid_08_where_compound_or_order_by(self):
        res = self.compiler.compile("SELECT * FROM students WHERE age >= 18 OR marks > 80 ORDER BY age;")
        self.assertTrue(res.is_success)
        self.assertEqual(len(res.errors), 0)

    def test_valid_case_insensitivity(self):
        res = self.compiler.compile("select NAME, AGE from STUDENTS where AGE > 18 order by AGE desc;")
        self.assertTrue(res.is_success)
        self.assertEqual(len(res.errors), 0)

    def test_valid_with_comments_and_formatting(self):
        sql = """
        -- Querying top performing students
        SELECT name, marks
        FROM students
        WHERE marks >= 85.5 /* high achievers */
        ORDER BY marks DESC;
        """
        res = self.compiler.compile(sql)
        self.assertTrue(res.is_success)
        self.assertEqual(len(res.errors), 0)

    # --------------------------------------------------------------------------
    # Mandated Invalid Test Cases (Part 13)
    # --------------------------------------------------------------------------

    def test_invalid_01_missing_column(self):
        res = self.compiler.compile("SELECT FROM students;")
        self.assertFalse(res.is_success)
        self.assertEqual(res.errors[0].error_type, "Syntax Error")
        self.assertEqual(res.phases["syntax"], "FAILED")

    def test_invalid_02_missing_from_keyword(self):
        res = self.compiler.compile("SELECT name students;")
        self.assertFalse(res.is_success)
        self.assertEqual(res.errors[0].error_type, "Syntax Error")

    def test_invalid_03_missing_table_name(self):
        res = self.compiler.compile("SELECT name FROM;")
        self.assertFalse(res.is_success)
        self.assertEqual(res.errors[0].error_type, "Syntax Error")

    def test_invalid_04_missing_where_condition(self):
        res = self.compiler.compile("SELECT name FROM students WHERE;")
        self.assertFalse(res.is_success)
        self.assertEqual(res.errors[0].error_type, "Syntax Error")

    def test_invalid_05_missing_order_by_column(self):
        res = self.compiler.compile("SELECT name FROM students ORDER BY;")
        self.assertFalse(res.is_success)
        self.assertEqual(res.errors[0].error_type, "Syntax Error")

    def test_invalid_06_unknown_column(self):
        res = self.compiler.compile("SELECT unknown_column FROM students;")
        self.assertFalse(res.is_success)
        self.assertEqual(res.errors[0].error_type, "Semantic Error")
        self.assertEqual(res.phases["semantic"], "FAILED")

    def test_invalid_07_unknown_table(self):
        res = self.compiler.compile("SELECT name FROM unknown_table;")
        self.assertFalse(res.is_success)
        self.assertEqual(res.errors[0].error_type, "Semantic Error")

    def test_invalid_08_missing_comparison_right_operand(self):
        res = self.compiler.compile("SELECT name FROM students WHERE age >;")
        self.assertFalse(res.is_success)
        self.assertEqual(res.errors[0].error_type, "Syntax Error")

    def test_invalid_09_invalid_character_lexical(self):
        res = self.compiler.compile("SELECT name FROM students @;")
        self.assertFalse(res.is_success)
        self.assertEqual(res.errors[0].error_type, "Lexical Error")
        self.assertEqual(res.phases["lexical"], "FAILED")

    def test_invalid_10_trailing_comma_select(self):
        res = self.compiler.compile("SELECT name, FROM students;")
        self.assertFalse(res.is_success)
        self.assertEqual(res.errors[0].error_type, "Syntax Error")

    def test_invalid_empty_query(self):
        res = self.compiler.compile("   ")
        self.assertFalse(res.is_success)
        self.assertEqual(res.errors[0].error_type, "Syntax Error")


if __name__ == "__main__":
    unittest.main()
