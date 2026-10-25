"""
Token definitions and data structures for the Mini SQL Compiler.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional


class TokenType(Enum):
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"
    OPERATOR = "OPERATOR"
    COMMA = "COMMA"
    SEMICOLON = "SEMICOLON"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    ASTERISK = "ASTERISK"
    EOF = "EOF"

    def __str__(self) -> str:
        return self.value


KEYWORDS = {
    "SELECT",
    "DISTINCT",
    "FROM",
    "WHERE",
    "ORDER",
    "BY",
    "ASC",
    "DESC",
    "AND",
    "OR",
    "NOT",
}

COMPARISON_OPERATORS = {
    "=",
    "!=",
    "<>",
    ">",
    "<",
    ">=",
    "<=",
}

LOGICAL_OPERATORS = {
    "AND",
    "OR",
    "NOT",
}


@dataclass
class Token:
    """Represents a lexical token generated from source SQL text."""
    type: TokenType
    value: str
    line: int
    column: int
    literal_value: Optional[Any] = None

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "lexeme": self.value,
            "line": self.line,
            "column": self.column,
            "literal_value": self.literal_value if self.literal_value is not None else self.value,
        }

    def __repr__(self) -> str:
        return f"Token({self.type.value}, '{self.value}', line={self.line}, col={self.column})"
