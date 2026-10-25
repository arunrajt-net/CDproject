"""
Error hierarchy and diagnostic reporting for the Mini SQL Compiler.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class CompilerError(Exception):
    """Base class for all compiler diagnostic errors."""
    error_type: str
    message: str
    line: int
    column: int
    suggestion: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_type": self.error_type,
            "message": self.message,
            "line": self.line,
            "column": self.column,
            "suggestion": self.suggestion,
        }

    def __str__(self) -> str:
        sugg = f" Suggestion: {self.suggestion}" if self.suggestion else ""
        return f"[{self.error_type}] Line {self.line}, Col {self.column}: {self.message}.{sugg}"


class LexicalError(CompilerError):
    """Raised when an unrecognized character or malformed token is encountered."""
    def __init__(self, message: str, line: int, column: int, suggestion: Optional[str] = None):
        super().__init__("Lexical Error", message, line, column, suggestion)


class SyntaxError(CompilerError):
    """Raised when the token stream violates Context-Free Grammar rules."""
    def __init__(self, message: str, line: int, column: int, suggestion: Optional[str] = None):
        super().__init__("Syntax Error", message, line, column, suggestion)


class SemanticError(CompilerError):
    """Raised when query fails semantic checks (unknown table, column, type mismatch)."""
    def __init__(self, message: str, line: int, column: int, suggestion: Optional[str] = None):
        super().__init__("Semantic Error", message, line, column, suggestion)
