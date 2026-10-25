"""
Lexical Analyzer for the Mini SQL Compiler.
Scans source SQL text, tracks line/column numbers, and produces a stream of validated tokens.
"""

from typing import List, Tuple, Optional
from .tokens import Token, TokenType, KEYWORDS, COMPARISON_OPERATORS
from .errors import LexicalError


class Lexer:
    """
    Finite-state lexical scanner for restricted SQL subset.
    Performs case-insensitive keyword recognition, string escaping,
    numeric literal parsing, operator detection, and comment skipping.
    """

    def __init__(self, source_code: str):
        self.source: str = source_code
        self.length: int = len(source_code)
        self.pos: int = 0
        self.line: int = 1
        self.column: int = 1
        self.tokens: List[Token] = []

    def _peek(self, offset: int = 0) -> Optional[str]:
        idx = self.pos + offset
        if idx < self.length:
            return self.source[idx]
        return None

    def _advance(self) -> str:
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def tokenize(self) -> List[Token]:
        self.tokens = []
        self.pos = 0
        self.line = 1
        self.column = 1

        while self.pos < self.length:
            ch = self._peek()

            # 1. Skip whitespace
            if ch.isspace():
                self._advance()
                continue

            # 2. SQL Comments: single-line (-- ...) and block (/* ... */)
            if ch == "-" and self._peek(1) == "-":
                self._skip_single_line_comment()
                continue
            if ch == "/" and self._peek(1) == "*":
                self._skip_block_comment()
                continue

            # 3. String literals (enclosed in single quotes)
            if ch == "'":
                self.tokens.append(self._scan_string())
                continue

            # 4. Numeric literals (Integers and Decimals)
            if ch.isdigit():
                self.tokens.append(self._scan_number())
                continue

            # 5. Multi-character and single-character comparison operators
            if ch in ("<", ">", "!", "="):
                token = self._scan_operator()
                if token:
                    self.tokens.append(token)
                    continue

            # 6. Single-character symbols: comma, semicolon, parentheses, asterisk
            if ch == "*":
                start_line, start_col = self.line, self.column
                self._advance()
                self.tokens.append(Token(TokenType.ASTERISK, "*", start_line, start_col, "*"))
                continue

            if ch == ",":
                start_line, start_col = self.line, self.column
                self._advance()
                self.tokens.append(Token(TokenType.COMMA, ",", start_line, start_col, ","))
                continue

            if ch == ";":
                start_line, start_col = self.line, self.column
                self._advance()
                self.tokens.append(Token(TokenType.SEMICOLON, ";", start_line, start_col, ";"))
                continue

            if ch == "(":
                start_line, start_col = self.line, self.column
                self._advance()
                self.tokens.append(Token(TokenType.LPAREN, "(", start_line, start_col, "("))
                continue

            if ch == ")":
                start_line, start_col = self.line, self.column
                self._advance()
                self.tokens.append(Token(TokenType.RPAREN, ")", start_line, start_col, ")"))
                continue

            # 7. Identifiers and Keywords
            if ch.isalpha() or ch == "_":
                self.tokens.append(self._scan_identifier_or_keyword())
                continue

            # 8. Unrecognized / Invalid Character Error
            start_line, start_col = self.line, self.column
            bad_char = self._advance()
            raise LexicalError(
                message=f"Unrecognized or invalid character '{bad_char}' in SQL query",
                line=start_line,
                column=start_col,
                suggestion=f"Remove character '{bad_char}' or replace with valid SQL syntax"
            )

        # Append End-Of-File token
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column, None))
        return self.tokens

    def _skip_single_line_comment(self) -> None:
        self._advance()  # -
        self._advance()  # -
        while self.pos < self.length and self._peek() != "\n":
            self._advance()

    def _skip_block_comment(self) -> None:
        start_line, start_col = self.line, self.column
        self._advance()  # /
        self._advance()  # *
        while self.pos < self.length:
            if self._peek() == "*" and self._peek(1) == "/":
                self._advance()
                self._advance()
                return
            self._advance()
        raise LexicalError(
            message="Unterminated block comment '/*'",
            line=start_line,
            column=start_col,
            suggestion="Close the block comment with '*/'"
        )

    def _scan_string(self) -> Token:
        start_line, start_col = self.line, self.column
        self._advance()  # Consume opening quote

        chars = []
        raw_lexeme = ["'"]

        while self.pos < self.length:
            ch = self._peek()

            if ch == "\n":
                raise LexicalError(
                    message="Unterminated string literal: newline found before closing quote",
                    line=start_line,
                    column=start_col,
                    suggestion="Close string literal before starting a new line"
                )

            if ch == "\\":  # Escape sequence
                raw_lexeme.append(self._advance())
                if self.pos >= self.length:
                    raise LexicalError(
                        message="Unterminated escape sequence at end of file",
                        line=self.line,
                        column=self.column,
                        suggestion="Provide an escape character or close string"
                    )
                esc = self._advance()
                raw_lexeme.append(esc)
                if esc == "'":
                    chars.append("'")
                elif esc == '"':
                    chars.append('"')
                elif esc == "\\":
                    chars.append("\\")
                elif esc == "n":
                    chars.append("\n")
                elif esc == "t":
                    chars.append("\t")
                elif esc == "r":
                    chars.append("\r")
                else:
                    raise LexicalError(
                        message=f"Invalid escape sequence '\\{esc}' in string literal",
                        line=self.line,
                        column=self.column - 1,
                        suggestion="Valid escapes are \\', \\\", \\\\, \\n, \\t, \\r"
                    )
                continue

            if ch == "'":
                raw_lexeme.append(self._advance())  # Consume closing quote
                literal_val = "".join(chars)
                return Token(
                    TokenType.STRING,
                    "".join(raw_lexeme),
                    start_line,
                    start_col,
                    literal_val
                )

            raw_lexeme.append(ch)
            chars.append(self._advance())

        raise LexicalError(
            message="Unterminated string literal: missing closing single quote (')",
            line=start_line,
            column=start_col,
            suggestion="Add a closing single quote (') to terminate the string"
        )

    def _scan_number(self) -> Token:
        start_line, start_col = self.line, self.column
        num_str = []
        has_dot = False

        while self.pos < self.length:
            ch = self._peek()
            if ch.isdigit():
                num_str.append(self._advance())
            elif ch == "." and not has_dot:
                # Check if next char is digit (e.g. 3.14)
                next_ch = self._peek(1)
                if next_ch and next_ch.isdigit():
                    has_dot = True
                    num_str.append(self._advance())  # '.'
                    num_str.append(self._advance())  # digit
                else:
                    break
            else:
                break

        # Check for malformed identifier following number, e.g. 18abc
        if self.pos < self.length and (self._peek().isalpha() or self._peek() == "_"):
            bad_id = []
            while self.pos < self.length and (self._peek().isalnum() or self._peek() == "_"):
                bad_id.append(self._advance())
            full_bad = "".join(num_str) + "".join(bad_id)
            raise LexicalError(
                message=f"Invalid numeric literal or identifier '{full_bad}': identifiers cannot start with numbers",
                line=start_line,
                column=start_col,
                suggestion="Separate number and identifier with whitespace or rename identifier"
            )

        raw = "".join(num_str)
        if has_dot:
            return Token(TokenType.NUMBER, raw, start_line, start_col, float(raw))
        return Token(TokenType.NUMBER, raw, start_line, start_col, int(raw))

    def _scan_operator(self) -> Optional[Token]:
        start_line, start_col = self.line, self.column
        ch = self._peek()

        if ch == "!":
            if self._peek(1) == "=":
                self._advance()
                self._advance()
                return Token(TokenType.OPERATOR, "!=", start_line, start_col, "!=")
            raise LexicalError(
                message="Unexpected character '!'. Did you mean '!='?",
                line=start_line,
                column=start_col,
                suggestion="Use '!=' for inequality"
            )

        if ch == "<":
            if self._peek(1) == ">":
                self._advance()
                self._advance()
                return Token(TokenType.OPERATOR, "<>", start_line, start_col, "<>")
            if self._peek(1) == "=":
                self._advance()
                self._advance()
                return Token(TokenType.OPERATOR, "<=", start_line, start_col, "<=")
            self._advance()
            return Token(TokenType.OPERATOR, "<", start_line, start_col, "<")

        if ch == ">":
            if self._peek(1) == "=":
                self._advance()
                self._advance()
                return Token(TokenType.OPERATOR, ">=", start_line, start_col, ">=")
            self._advance()
            return Token(TokenType.OPERATOR, ">", start_line, start_col, ">")

        if ch == "=":
            self._advance()
            return Token(TokenType.OPERATOR, "=", start_line, start_col, "=")

        return None

    def _scan_identifier_or_keyword(self) -> Token:
        start_line, start_col = self.line, self.column
        chars = []

        while self.pos < self.length:
            ch = self._peek()
            if ch.isalnum() or ch == "_":
                chars.append(self._advance())
            else:
                break

        lexeme = "".join(chars)
        upper_lexeme = lexeme.upper()

        if upper_lexeme in KEYWORDS:
            return Token(
                TokenType.KEYWORD,
                lexeme,
                start_line,
                start_col,
                upper_lexeme  # normalized uppercase
            )

        return Token(
            TokenType.IDENTIFIER,
            lexeme,
            start_line,
            start_col,
            lexeme
        )
