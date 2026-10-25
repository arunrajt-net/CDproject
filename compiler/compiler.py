"""
Master Compiler Driver for the Mini SQL Compiler.
Coordinates Lexical Analysis, Syntax Analysis, Parse Tree Generation,
Semantic Analysis, and Symbol Table Management.
"""

import time
from typing import Dict, Any, List, Optional
from pathlib import Path

from .tokens import Token
from .lexer import Lexer
from .parser import Parser
from .parse_tree import ParseTreeNode
from .ast_nodes import QueryNode
from .symbol_table import SymbolTable
from .semantic_analyzer import SemanticAnalyzer
from .errors import CompilerError, LexicalError, SyntaxError, SemanticError


class CompilationResult:
    """Encapsulates the end-to-end outcome of a compilation run."""

    def __init__(
        self,
        source_query: str,
        is_success: bool,
        tokens: List[Token],
        parse_tree: Optional[ParseTreeNode] = None,
        ast: Optional[QueryNode] = None,
        semantic_report: Optional[Dict[str, Any]] = None,
        symbol_table_entries: Optional[List[Dict[str, Any]]] = None,
        errors: Optional[List[CompilerError]] = None,
        phases: Optional[Dict[str, str]] = None,
        duration_ms: float = 0.0,
    ):
        self.source_query = source_query
        self.is_success = is_success
        self.tokens = tokens
        self.parse_tree = parse_tree
        self.ast = ast
        self.semantic_report = semantic_report or {}
        self.symbol_table_entries = symbol_table_entries or []
        self.errors = errors or []
        self.phases = phases or {
            "lexical": "PENDING",
            "syntax": "PENDING",
            "semantic": "PENDING",
        }
        self.duration_ms = duration_ms

    def to_dict(self) -> Dict[str, Any]:
        """Converts compilation outcome to a JSON-ready dictionary for frontend API."""
        return {
            "success": self.is_success,
            "source_query": self.source_query,
            "tokens": [t.to_dict() for t in self.tokens],
            "token_count": len([t for t in self.tokens if t.type.value != "EOF"]),
            "parse_tree_text": self.parse_tree.to_text_tree() if self.parse_tree else None,
            "parse_tree_json": self.parse_tree.to_dict() if self.parse_tree else None,
            "ast_text": self.ast.to_text_tree() if self.ast else None,
            "ast_json": self.ast.to_dict() if self.ast else None,
            "semantic_analysis": self.semantic_report,
            "symbol_table": self.symbol_table_entries,
            "errors": [err.to_dict() for err in self.errors],
            "phases": self.phases,
            "duration_ms": round(self.duration_ms, 2),
        }


class MiniSQLCompiler:
    """
    Main Compiler Engine providing end-to-end compilation services for Mini SQL queries.
    """

    def __init__(self, schema_path: Optional[str] = None):
        if schema_path:
            self.symbol_table = SymbolTable.load_from_file(schema_path)
        else:
            # Fallback default schema matching specification
            default_schema = {
                "students": {
                    "columns": {
                        "id": {"type": "INT", "nullable": False, "primary_key": True},
                        "name": {"type": "VARCHAR", "nullable": False},
                        "age": {"type": "INT", "nullable": True},
                        "department": {"type": "VARCHAR", "nullable": True},
                        "marks": {"type": "FLOAT", "nullable": True},
                    },
                    "description": "Student academic and personal records",
                },
                "employees": {
                    "columns": {
                        "id": {"type": "INT", "nullable": False, "primary_key": True},
                        "name": {"type": "VARCHAR", "nullable": False},
                        "salary": {"type": "FLOAT", "nullable": True},
                        "department": {"type": "VARCHAR", "nullable": True},
                    },
                    "description": "Company employee payroll and department records",
                },
            }
            self.symbol_table = SymbolTable(default_schema)

        self.semantic_analyzer = SemanticAnalyzer(self.symbol_table)

    def compile(self, query_string: str) -> CompilationResult:
        """
        Compiles an input SQL query through all compiler front-end stages.
        """
        start_time = time.perf_counter()
        phases = {
            "lexical": "PENDING",
            "syntax": "PENDING",
            "semantic": "PENDING",
        }
        tokens: List[Token] = []
        parse_tree: Optional[ParseTreeNode] = None
        ast: Optional[QueryNode] = None
        semantic_report: Optional[Dict[str, Any]] = None
        errors: List[CompilerError] = []

        # ----------------------------------------------------
        # Stage 1: Lexical Analysis
        # ----------------------------------------------------
        try:
            lexer = Lexer(query_string)
            tokens = lexer.tokenize()
            phases["lexical"] = "PASSED"
        except LexicalError as le:
            phases["lexical"] = "FAILED"
            phases["syntax"] = "SKIPPED"
            phases["semantic"] = "SKIPPED"
            errors.append(le)
            elapsed = (time.perf_counter() - start_time) * 1000
            return CompilationResult(
                source_query=query_string,
                is_success=False,
                tokens=tokens,
                symbol_table_entries=self.symbol_table.get_all_entries(),
                errors=errors,
                phases=phases,
                duration_ms=elapsed,
            )

        # ----------------------------------------------------
        # Stage 2: Syntax Analysis & Parse Tree Generation
        # ----------------------------------------------------
        try:
            parser = Parser(tokens)
            parse_tree, ast = parser.parse()
            phases["syntax"] = "PASSED"
        except SyntaxError as se:
            phases["syntax"] = "FAILED"
            phases["semantic"] = "SKIPPED"
            errors.append(se)
            elapsed = (time.perf_counter() - start_time) * 1000
            return CompilationResult(
                source_query=query_string,
                is_success=False,
                tokens=tokens,
                parse_tree=parse_tree,
                symbol_table_entries=self.symbol_table.get_all_entries(),
                errors=errors,
                phases=phases,
                duration_ms=elapsed,
            )

        # ----------------------------------------------------
        # Stage 3: Semantic Analysis & Schema Validation
        # ----------------------------------------------------
        try:
            semantic_report = self.semantic_analyzer.analyze(ast)
            phases["semantic"] = "PASSED"
        except SemanticError as sme:
            phases["semantic"] = "FAILED"
            errors.append(sme)
            elapsed = (time.perf_counter() - start_time) * 1000
            return CompilationResult(
                source_query=query_string,
                is_success=False,
                tokens=tokens,
                parse_tree=parse_tree,
                ast=ast,
                symbol_table_entries=self.symbol_table.get_all_entries(),
                errors=errors,
                phases=phases,
                duration_ms=elapsed,
            )

        elapsed = (time.perf_counter() - start_time) * 1000
        return CompilationResult(
            source_query=query_string,
            is_success=True,
            tokens=tokens,
            parse_tree=parse_tree,
            ast=ast,
            semantic_report=semantic_report,
            symbol_table_entries=self.symbol_table.get_all_entries(),
            errors=[],
            phases=phases,
            duration_ms=elapsed,
        )
