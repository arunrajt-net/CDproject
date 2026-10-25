# Lexical Analysis (Scanning)

## 1. Principles of Lexical Analysis
Lexical Analysis is the first phase of the compiler front-end. Its fundamental responsibility is to read the source program as a continuous stream of characters and group them into meaningful minimum grammatical units called **tokens**.

Key concepts:
- **Token:** An abstract symbol representing a category of lexical element (e.g. `KEYWORD`, `IDENTIFIER`, `NUMBER`).
- **Lexeme:** The actual sequence of characters in the source text matching the pattern for a token (e.g. `SELECT`, `age`, `42`).
- **Pattern:** The formal rule or regular expression defining how a token is constructed.

---

## 2. Implementation in Mini SQL Compiler (`compiler/lexer.py`)

The scanner operates as a hand-crafted deterministic finite automaton (DFA) through a single traversal of the query string.

### 2.1 State Flow
1. **Whitespace Elimination:** Spaces, tabs (`\t`), and carriage returns (`\r`) increment the column counter and are skipped. Newlines (`\n`) increment the line counter and reset the column counter to 1.
2. **Comment Stripping:**
   - Single-line comments (`-- ...`) skip characters until a newline is reached.
   - Multi-line block comments (`/* ... */`) skip characters until the closing `*/` sequence is found.
3. **Keyword & Identifier Recognition:**
   - When an alphabetic character or underscore `_` is encountered, characters are accumulated until a non-alphanumeric character is reached.
   - The lexeme is normalized to uppercase. If it exists in the set of SQL keywords (`SELECT`, `FROM`, etc.), a `KEYWORD` token is emitted. Otherwise, an `IDENTIFIER` token is emitted preserving original casing.
4. **Number Parsing:**
   - Sequences of digits are accumulated. If a decimal point `.` followed by additional digits is seen, a floating-point number is parsed; otherwise an integer is parsed.
   - If letters immediately follow digits without whitespace (e.g. `123name`), a diagnostic `LexicalError` is raised.
5. **String Literal Escaping:**
   - Begins upon encountering `'`. Characters are gathered until a matching `'` is found.
   - Backslashes trigger escape processing (`\'`, `\"`, `\\`, `\n`, `\t`).
   - Unterminated strings (EOF or newline before closing quote) raise an explicit `LexicalError`.
6. **Comparison Operators:**
   - Multi-character operators (`!=`, `<>`, `<=`, `>=`) are inspected using a 1-character lookahead (`_peek(1)`).
   - Single-character operators (`=`, `<`, `>`) are parsed directly.

---

## 3. Lexical Token Categories

| Token Type | Recognized Lexemes | Example In Source |
|---|---|---|
| `KEYWORD` | `SELECT`, `DISTINCT`, `FROM`, `WHERE`, `ORDER`, `BY`, `ASC`, `DESC`, `AND`, `OR`, `NOT` | `SELECT`, `from`, `Where` |
| `IDENTIFIER` | `[a-zA-Z_][a-zA-Z0-9_]*` | `students`, `salary_2026`, `age` |
| `NUMBER` | `[0-9]+` or `[0-9]+\.[0-9]+` | `18`, `80.5`, `30000` |
| `STRING` | `'(\\'|.)*?'` | `'CSE'`, `'Hello World'` |
| `OPERATOR` | `=`, `!=`, `<>`, `>`, `<`, `>=`, `<=` | `>=`, `<>`, `=` |
| `COMMA` | `,` | `,` |
| `SEMICOLON` | `;` | `;` |
| `LPAREN` | `(` | `(` |
| `RPAREN` | `)` | `)` |
| `ASTERISK` | `*` | `*` |
| `EOF` | End-of-file | (Sentinel) |
